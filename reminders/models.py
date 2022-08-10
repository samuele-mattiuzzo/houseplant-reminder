import datetime
import random

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

NEVER = 0
ONE_HOUR = 1
ONE_DAY = 2
ONE_WEEK = 3
ONE_MONTH = 4
REPEAT_CHOICES = (
    (NEVER, 'never'),
    (ONE_HOUR, '1 hour'),
    (ONE_DAY, '1 day'),
    (ONE_WEEK, '1 week'),
    (ONE_MONTH, '1 month'),
)


class Task(models.Model):
    title = models.CharField(max_length=200)
    repeat_every = models.CharField(
        max_length=200, choices=REPEAT_CHOICES, default=NEVER)
    color = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return self.title

    def _generate_color_code(self):
        return '#' + str(hex(random.randint(0, 16777215)))[2:]

    def save(self, *args, **kwargs):
        self.color = self._generate_color_code()
        return super().save(*args, **kwargs)


class ScheduledTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField('date created', auto_now_add=True)
    due_date = models.DateTimeField('due date')
    completed_date = models.DateTimeField('due date', blank=True)

    def __str__(self):
        return "{} is due on {}".format(self.task, self.due_date)

    @property
    def time_left(self):
        difference = self.scheduled_date - datetime.datetime.now()
        d = divmod(difference, 86400)  # days
        h = divmod(d[1], 3600)  # hours
        m = divmod(h[1], 60)  # minutes
        s = m[1]  # seconds

        return (d[0], h[0], m[0], s)

    def mark_complete(self):
        self.completed_date = datetime.datetime.now()
        self.save()

    def _get_next_due_date(self):
        rpt = self.task.repeats_every
        if rpt == NEVER:
            return None
        else:
            if rpt == ONE_HOUR:
                return self.completed_date + datetime.timedelta(hours=1)
            elif rpt == ONE_DAY:
                return self.completed_date + datetime.timedelta(days=1)
            elif rpt == ONE_WEEK:
                return self.completed_date + datetime.timedelta(days=7)
            elif rpt == ONE_MONTH:
                return self.completed_date + datetime.timedelta(months=1)

    def reschedule(self):
        return ScheduledTask.objects.create(
            task=self.task,
            scheduled_date=self.completed_date,
            due_date=self._get_next_due_date()
        )

    def save(self, *args, **kwargs):
        if self.task.repeats_every != NEVER:
            self.reschedule()
        return super().save(*args, **kwargs)
