import random


class Student:
    """Represents a student driving to Columbia College

    Attributes
    ----------
    sid : int
        Student ID
    expected_arrival_time : int
        When a student intends to arrive to campus (consistent throughout all days of the model).
        Measured in seconds since campus opens.
    daily_arrival_time : int
        When a student actually shows up (changes each morning they need to come to campus)
        Measured in seconds since campus opens.
    view_duration : int
        How long a student will see the sign (changes each morning they need to come to campus)
        Measured in seconds.
    departure_time : int
        When a student will no longer be able to see the sign (changes as daily_arrival_time and view_duration changes)
        Mesured in seconds since campus opens.
    signs_seen : list
        A list of signs that a student has seen during the models run.

    Methods
    -------
    summary
        prints high level information about a student in the model
    """
    def __init__(self, model, sid, arrival_time):
        # Capture a reference to the model to access it's attributes
        self.model = model

        # Give each student a Student ID
        self.sid = sid

        # When will they usually show up to campus
        self.expected_arrival_time = arrival_time

        # Randomly assign them days of the week to attend school
        self.arrival_days = random.sample(self.model.config.get("weekdays"),
                                          self.model.config.get("school_days"))
        self.arrival_days.sort()

        # Tracks the slides a given student has seen
        self.signs_seen = []

    def start_day(self):
        """What happens each day when a student comes to campus"""
        self.set_daily_arrival_time()
        self.set_daily_view_duration()
        self.set_daily_departure_time()

    def view_sign(self, sign):
        """Adds a sign to students list of seen signs"""
        if sign not in self.signs_seen:
            self.signs_seen.append(sign)

    def set_daily_view_duration(self):
        """Sets a students daily view duration.

        Daily view duration is how long a student will see the sign (changes each morning they need to come to campus)
        Measured in seconds.
        """
        self.view_duration = int(random.gauss(self.model.config.get("duration_visibility"),
                                              self.model.config.get("sd_visibility")))

    def set_daily_arrival_time(self):
        """Sets a students daily arrival time.

        Daily arrival time is when a student actually shows up (changes each morning they need to come to campus)
        Measured in seconds since campus opens.
        """
        diff = int(random.gauss(self.model.config.get("duration_timely"),
                                self.model.config.get("sd_timely")))
        new_time = self.expected_arrival_time + diff

        # Hack way to account for students with early start times combined with a negative diff
        self.daily_arrival_time = 0 if new_time < 0 else new_time

    def set_daily_departure_time(self):
        """Sets a students departure time.

        Departure Time is when a student will no longer be able to see the sign
        (changes as daily_arrival_time and view_duration changes)
        """
        self.departure_time = self.daily_arrival_time + self.view_duration

    def __lt__(self, other):
        """This overrides how students can be sorted"""
        return self.daily_arrival_time < other.daily_arrival_time

    def __str__(self):
        return f"Student {self.sid} (Signs Viewed: {len(self.signs_seen)})"
