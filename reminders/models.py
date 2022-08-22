import datetime
import random

from django.db import models
from django.utils import timezone

from .constants import *


class Plant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    flowered = models.BooleanField(default=False)
    feed_repeat_every = models.CharField(
        max_length=200, choices=REPEAT_CHOICES, default=NEVER)
    water_repeat_every = models.CharField(
        max_length=200, choices=REPEAT_CHOICES, default=NEVER)
    color = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return self.name

    def _generate_color_code(self):
        return random.choice(COLORS)

    @property
    def schedule(self):
        return self.scheduled_plant.first()

    @property
    def water_repeat_every_human(self):
        return REPEAT_CHOICES[int(self.water_repeat_every)][1]

    @property
    def feed_repeat_every_human(self):
        return REPEAT_CHOICES[int(self.feed_repeat_every)][1]

    def save(self, *args, **kwargs):
        self.color = self._generate_color_code()
        return super().save(*args, **kwargs)


class ScheduledPlant(models.Model):
    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name='scheduled_plant')
    scheduled_feed_date = models.DateTimeField(
        'date for next refeed', null=True, blank=True)
    scheduled_water_date = models.DateTimeField(
        'date for next water', null=True, blank=True)
    last_feed = models.DateTimeField(
        'date last fed', null=True, blank=True)
    last_water = models.DateTimeField(
        'date last watered', null=True, blank=True)

    def __str__(self):
        return "Schedule for {}".format(self.plant.name)

    @property
    def feed_time_left(self):
        return self._time_left(
            self.scheduled_feed_date
        )

    @property
    def water_time_left(self):
        return self._time_left(
            self.scheduled_water_date
        )

    @property
    def feed_time_left_percent(self):
        return self._time_left_percent(FEED_ACTION)

    @property
    def water_time_left_percent(self):
        return self._time_left_percent(WATER_ACTION)

    def mark_feed(self):
        self._update_next_due_for_action(FEED_ACTION)
        self.last_feed = timezone.now()
        self.save()

    def mark_water(self):
        self._update_next_due_for_action(WATER_ACTION)
        self.last_water = timezone.now()
        self.save()

    def _time_left_seconds(self, date):
        difference = date - timezone.now()
        return difference.total_seconds()

    def _time_left(self, date):
        days = divmod(self._time_left_seconds(date), 86400)  # days
        hours = divmod(days[1], 3600)  # hours

        return (int(days[0]), int(hours[0]))

    def _time_left_percent(self, action_type=WATER_ACTION):
        due_date_seconds = self.scheduled_feed_date if action_type == FEED_ACTION else self.scheduled_water_date
        time_left_seconds = self._time_left_seconds(
            self.scheduled_feed_date) if action_type == FEED_ACTION else self._time_left_seconds(
            self.scheduled_water_date)

        epoch = timezone.make_aware(
            datetime.datetime(1970, 1, 1))
        due_date_seconds = (due_date_seconds - epoch).total_seconds()
        res = (100 - int(
            due_date_seconds/(100*time_left_seconds)
        ))
        return res

    def _update_next_due_for_action(self, action_type=WATER_ACTION, first_update=False):

        if action_type == WATER_ACTION:
            rpt = self.plant.water_repeat_every
            last_action = self.last_water if self.last_water is not None else timezone.now()
        else:
            rpt = self.plant.feed_repeat_every
            last_action = self.last_feed if self.last_feed is not None else timezone.now()

        if rpt == NEVER:
            return
        else:
            if rpt == ONE_HOUR:
                res = last_action + datetime.timedelta(hours=1)
            else:
                if rpt == ONE_DAY: days = 1
                elif rpt == ONE_WEEK: days = 7
                elif rpt == ONE_MONTH: days = 30
                elif rpt == OTHER_DAY: days = 2
                elif rpt == OTHER_WEEK: days = 14
                res = last_action + datetime.timedelta(days=days)

        if action_type == WATER_ACTION:
            self.scheduled_water_date = res
            if first_update:
                self.last_water = res
        else:
            self.scheduled_feed_date = res
            if first_update:
                self.last_feed = res

    def save(self, *args, **kwargs):
        if not self.scheduled_feed_date:
            self._update_next_due_for_action(FEED_ACTION, True)

        if not self.scheduled_water_date:
            self._update_next_due_for_action(WATER_ACTION, True)

        return super().save(*args, **kwargs)
