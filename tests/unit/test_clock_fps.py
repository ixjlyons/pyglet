
"""Tests clock timing between frames and estimations
of frames per second.
"""

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import time
import unittest

from pyglet import clock


def sleep(seconds):
    """Busy sleep on the CPU which is very precise"""
    pyclock = clock.get_default()
    start = pyclock.time()
    while pyclock.time() - start < seconds:
        pass


class ClockTimingTestCase(unittest.TestCase):

    def setUp(self):
        # since clock is global,
        # we initialize a new clock on every test
        clock.set_default(clock.Clock())

    def test_first_tick_is_delta_zero(self):
        """
        Tests that the first tick is dt = 0.
        """
        dt = clock.tick()
        self.assertTrue(dt == 0)

    def test_start_at_zero_fps(self):
        """
        Tests that the default clock starts
        with zero fps.
        """
        self.assertTrue(clock.get_fps() == 0)

    def test_elapsed_time_between_tick(self):
        """
        Test that the tick function returns the correct elapsed
        time between frames, in seconds.

        Because we are measuring time differences, we
        expect a small error (1%) from the expected value.
        """
        sleep_time = 0.2

        # initialize internal counter
        clock.tick()

        # test between initialization and first tick
        sleep(sleep_time)
        delta_time_1 = clock.tick()

        # test between non-initialization tick and next tick
        sleep(sleep_time)
        delta_time_2 = clock.tick()

        self.assertAlmostEqual(delta_time_1, sleep_time, delta=0.01*sleep_time)
        self.assertAlmostEqual(delta_time_2, sleep_time, delta=0.01*sleep_time)

    def test_compute_fps(self):
        """
        Test that the clock computes a reasonable value of
        frames per second when simulated for 120 ticks at 60 frames per second.

        Because sleep is not very precise and fps are unbounded, we
        expect a moderate error (10%) from the expected value.
        """
        ticks = 120  # for averaging
        expected_fps = 60
        seconds_per_tick = 1./expected_fps

        for i in range(ticks):
            time.sleep(seconds_per_tick)
            clock.tick()
        computed_fps = clock.get_fps()

        self.assertAlmostEqual(computed_fps, expected_fps, delta=0.1*expected_fps)
