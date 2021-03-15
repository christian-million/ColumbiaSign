from linkedlist import LinkedList
from Student import Student
import json
import random
import datetime


class Schedule:
    '''A helper class to keep track of which students show up on which days.
    Intended to be run after Student init and helps avoid traversing all students on each day of a models run
    '''
    def __init__(self, weekdays=[1, 2, 3, 4, 5]):
        self.weekdays = {i: [] for i in weekdays}

    def add(self, student, days):
        for day in days:
            self.weekdays[day].append(student)

    def get_students(self, day):
        # Return a new list of student references to avoid modifying the Schedule weekdays dict entry
        return [student for student in self.weekdays.get(day)]


class Model:
    """Model to simulate student viewing the Columbia College sign.

    Attributes
    ----------
    sign : LinkedList
        Represents a sign that switches between n_slides
    students : list
        A list of Student objects, representing the students attending Columbia College

    Methods
    -------
    run
        Runs a model given parameters assigned on initialization.
    summary
        Summarizes the model results
    """
    def __init__(self, config="config.json"):

        # Loads all configurable variables
        with open(config) as f:
            config_verbose = json.load(f)
            self.config = {key: value.get("value") for key, value in config_verbose.items()}

        # Creates a Sign with `n_slides` slides
        self.sign = LinkedList([i for i in range(self.config.get("n_slides"))])
        self.sign.to_circle()
        self.active_sign = self.sign.head

        # The students actively viewing the signs
        self.viewing_queue = []

        # List of students
        self.students = []
        self.daily_students = []
        self.schedule = Schedule(weekdays=self.config.get("weekdays"))

        # The number of second the model runs each day
        self.seconds = self.calc_seconds(self.config.get("daily_start_time"), self.config.get("daily_end_time"))

        # A list of arrival times, used to instantiate students
        arrival = self.generate_arrival_times(self.config.get("n_students"),
                                              self.seconds)

        # Initialize list of students given the arrival times.
        for s, student in zip(arrival, range(self.config.get("n_students"))):
            self.students.append(Student(self, student, s))

        # Set the schedule
        for student in self.students:
            self.schedule.add(student, student.arrival_days)

    def calc_seconds(self, start_time, end_time, form="%H:%M"):
        '''Calculates the number of seconds (int) between two times'''
        start = datetime.datetime.strptime(start_time, form)
        end = datetime.datetime.strptime(end_time, form)
        duration = end - start
        s = int(duration.total_seconds())
        return s

    def generate_arrival_times(self, n_students, seconds):
        '''Generates a list of arrival times (in seconds since time=0) without replacement.'''
        arrival_times = random.sample(list(range(1, seconds + 1)), k=n_students)
        arrival_times.sort()
        return arrival_times

    def each_day(self, day):
        """Dictates what happens each day of the week."""
        # Determine whether to reset the sign or not
        if self.config.get("sign_reset"):
            self.active_sign = self.sign.head

        # Get a list of students expected to be on campus today
        self.daily_students = self.schedule.get_students(day)

        # Initializes arrival time, sign viewing duration, and departure time for each student
        # These values fluxuate daily for students.
        for student in self.daily_students:
            student.start_day()

        # Sorts the students based on arrival time
        self.daily_students.sort()

        # When will the last student be on campus?
        final_departure = max(self.daily_students, key=lambda x: x.departure_time)

        for s in range(final_departure.departure_time + 1):
            # Remove departed students
            self.remove_departed(s)

            # Add students who begin to view sign as second s
            self.add_to_queue(s)

            # Change the sign
            if s % self.config.get("duration_cycle") == 0:
                self.active_sign = self.active_sign.nxt

            for student in self.viewing_queue:
                student.view_sign(self.active_sign)

    def remove_departed(self, seconds):
        """This removes students from the viewing queue if they have 'passed' the sign"""
        removal_index = []

        # Identify students to remove
        for i, student in enumerate(self.viewing_queue):
            if student.departure_time == seconds:
                removal_index.append(i)

        # Traverse in reverse so indexing isn't messed up by previous removals
        for ri in sorted(removal_index, reverse=True):
            self.viewing_queue.pop(ri)

    def add_to_queue(self, s):
        """Adds students who arrive at second 's' to the viewing queue."""
        # Add new arrivals
        for i, student in enumerate(self.daily_students):
            if s == student.daily_arrival_time:
                # Add to viewing queue while removing from daily queue
                self.viewing_queue.append(self.daily_students.pop(i))

    def run(self):
        """This runs the model using the parameters supplied on initialization"""

        for week in range(self.config.get("weeks")):

            for day in self.config.get("weekdays"):

                self.each_day(day)

    def summary(self):
        """Returns a summary of the signs seen by students."""

        signs_seen = [len(student.signs_seen) for student in self.students]

        return {
            "n_students": len(self.students),
            "min_signs_viewed": min(signs_seen),
            "max_signs_viewed": max(signs_seen),
            "avg_signs_viewed": sum(signs_seen) / len(signs_seen),
            # Sorry about this one...
            "dist_signs_viewed": {slide: sum([1 for i in signs_seen if i == slide]) for slide in range(self.config.get("n_slides"))}
        }


if __name__ == '__main__':

    model = Model()

    model.run()

    print(model.summary())

    for i in [0, 1, 40, 44]:
        print(f"-------- STUDENT {i} ------------")
        student = model.students[i]
        print(student)
