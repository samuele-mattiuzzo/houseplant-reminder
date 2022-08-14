
from django.test import TestCase
from django.utils import timezone

from reminders.constants import *
from reminders.models import Plant, ScheduledPlant


class PlantTestCase(TestCase):
    def setUp(self):
        self.plant = Plant.objects.create(
            name="test plant",
            description="test plant description",
            feed_repeat_every=ONE_MONTH,
            water_repeat_every=ONE_WEEK
        )

    def test_plants_have_random_color(self):
        """Plants are created with a random color"""
        self.assertIsNotNone(self.plant.color)
        self.assertIn(self.plant.color, COLORS)

    def test_plants_have_human_version_of_repeats(self):
        self.assertEqual(
            self.plant.water_repeat_every_human,
            'once a week'
        )
        self.assertEqual(
            self.plant.feed_repeat_every_human,
            'once a month'
        )


class PlantScheduleTestCase(TestCase):
    def setUp(self):
        self.plant = Plant.objects.create(
            name="test plant",
            description="test plant description",
            feed_repeat_every=ONE_MONTH,
            water_repeat_every=ONE_WEEK
        )
        self.schedule = ScheduledPlant.objects.create(
            plant=self.plant
        )

    def test_schedule_is_created_with_next_dates(self):
        self.assertIsNotNone(
            self.schedule.scheduled_feed_date
        )
        self.assertIsNotNone(
            self.schedule.scheduled_water_date
        )

    def test_schedule_time_left_are_touples(self):
        self.assertIsNotNone(
            self.schedule.feed_time_left
        )
        self.assertIsNotNone(
            self.schedule.water_time_left
        )

    def test_schedule_time_left_percent_returns_int(self):
        self.assertTrue((
            self.schedule.feed_time_left_percent > 0 and
            self.schedule.feed_time_left_percent <= 100))

        self.assertTrue((
            self.schedule.water_time_left_percent > 0 and
            self.schedule.water_time_left_percent <= 100))

    def test_mark_feed_updates_dates(self):

        old_schedule = ScheduledPlant.objects.create(
            plant=self.plant,
            scheduled_feed_date=timezone.datetime(2012, 3, 3, 1, 30),
            scheduled_water_date=timezone.datetime(2012, 3, 3, 1, 30)
        )
        self.assertTrue(
            old_schedule.last_feed is None
        )
        self.assertTrue(
            old_schedule.last_water is None
        )

        current_feed = old_schedule.scheduled_feed_date
        current_water = old_schedule.scheduled_water_date

        old_schedule.mark_feed()
        old_schedule.mark_water()

        self.assertTrue(
            old_schedule.last_feed is not None
        )
        self.assertTrue(
            old_schedule.last_water is not None
        )
        self.assertNotEqual(
            old_schedule.scheduled_feed_date, current_feed
        )
        self.assertNotEqual(
            old_schedule.scheduled_water_date, current_water
        )
