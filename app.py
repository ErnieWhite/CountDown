import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import calendar
from datetime import date
from typing import Any
from tkinter import Menu

"""Finds actual meet up date based on a date description
For example, if given "1st Monday of January 2022", the correct meetup date is January 3, 2022.
"""


# subclassing the built-in ValueError to create MeetupDayException
class MeetupDayException(ValueError):
    """Exception raised when the Meetup weekday and count do not result in a valid date.

    message: explanation of the error.

    """
    def __init__(self, message):
        self.message = message


class MeetupDate:
    """Finds actual meet up date based on a date description

    For example, if given "1st Monday of January 2022", the correct meetup date is January 3, 2022.
    """

    @staticmethod
    def find_last_occurrence(year, month, week_day):
        """Finds the last occurrence of week_day in the month

        :param year: the year of the meetup
        :param month: the month of the meetup
        :param week_day: the last
        :return datetime.date: The date of the last meetup week_day
        """

        # create a calendar to work with
        my_calendar = calendar.Calendar(calendar.SUNDAY)

        # A 2d list that contains the days of the month in their proper positions in the week
        weeks = my_calendar.monthdayscalendar(year, month)

        for week in weeks[::-1]:  # reverse the weeks to find the last occurrence
            if week[week_day] != 0:  # the first time this is not zero is the last occurrence
                return date(year, month, week[week_day])

    @staticmethod
    def find_teenth_occurrence(year, month, week_day):
        """Finds the week_day in teens of the month. Their are 7 days in the range 13-19

        :param year: the year of the meetup
        :param month: the month of the meetup
        :param week_day: the day of the week that the meetup will occur
        :return datetime.date: The actual date of the meetup
        """

        # create a calendar to work with
        my_calendar = calendar.Calendar(calendar.SUNDAY)

        # A 2d list that contains the days of the month in their proper positions in the week
        weeks = my_calendar.monthdayscalendar(year, month)

        # search through the weeks until we find a day of the week with a day of the month in the teens
        for week in weeks:
            if 13 <= week[week_day] <= 19:
                return date(year, month, week[week_day])

    @staticmethod
    def find_nth_occurrence(year, month, week_day, occurrence):
        """Finds the nth week_day of the month

        :param year: The year of the meetup
        :param month: The month of the meetup
        :param week_day: The day of the week for the meetup
        :param occurrence: The nth occurrence of the day of the week
        :return datetime.date: The actual date of the meetup
        """

        # create a calendar to work with
        my_calendar = calendar.Calendar(calendar.SUNDAY)

        # A 2d list that contains the days of the month in their proper positions in the week
        weeks = my_calendar.monthdayscalendar(year, month)

        # a counter to keep track of how many the day of the week we have seen so far
        count = 0
        for week in weeks:
            if week[week_day] != 0:
                count += 1
                if count == occurrence:  # nth occurrence?
                    return date(year, month, week[week_day])
        raise MeetupDayException('That day does not exist.')

    @staticmethod
    def meetup(year, month, week, day_of_week):
        occurrences = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'teenth': 13, 'last': 99}
        days_of_week = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6}
        occurrence = occurrences[week]
        week_day = days_of_week[day_of_week]

        # find the last occurrence of the day of week
        if occurrence == 99:  # the last occurrence
            return MeetupDate.find_last_occurrence(year, month, week_day)

        if occurrence == 13:  # the teenth day
            return MeetupDate.find_teenth_occurrence(year, month, week_day)

        # the first through fifth occurrence
        return MeetupDate.find_nth_occurrence(year, month, week_day, occurrence)


class SimpleTimerSet(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        tk.Label(self, text="Hello from the simple timer setup").pack()

        self.pack()


class MeetupTimerSet(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        tk.Label(self, text="Hello from the meetup timer setup").pack()

        self.pack()


class DigitLabel(tk.Label):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self['background'] = 'black'
        self['foreground'] = 'green'
        self['text'] = '00'


class CountDownDisplay(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # create the widgets
        self.years_label = DigitLabel(self)
        self.months_label = DigitLabel(self)
        self.days_label = DigitLabel(self)

        self.hours_label = DigitLabel(self)
        self.minutes_label = DigitLabel(self)
        self.seconds_label = DigitLabel(self)

        # add the widgets
        # years, months, days
        self.years_label.grid(row=0, column=0, padx=5, pady=(5, 0))
        tk.Label(self, text='|').grid(row=0, column=1, pady=(3, 0))
        self.months_label.grid(row=0, column=2, padx=5, pady=(5, 0))
        tk.Label(self, text='|').grid(row=0, column=3, pady=(3, 0))
        self.days_label.grid(row=0, column=4, padx=5, pady=(5, 0))

        tk.Label(self, text='Y').grid(row=1, column=0)
        tk.Label(self, text='M').grid(row=1, column=2)
        tk.Label(self, text='D').grid(row=1, column=4)

        # hours, minutes, seconds
        self.hours_label.grid(row=2, column=0, padx=5, pady=(5, 0))
        tk.Label(self, text='|').grid(row=2, column=1, pady=(3, 0))
        self.minutes_label.grid(row=2, column=2, padx=5, pady=(5, 0))
        tk.Label(self, text='|').grid(row=2, column=3, pady=(3, 0))
        self.seconds_label.grid(row=2, column=4, padx=5, pady=(5, 0))

        tk.Label(self, text='H').grid(row=3, column=0)
        tk.Label(self, text='M').grid(row=3, column=2)
        tk.Label(self, text='S').grid(row=3, column=4)


class SimpleTimer(tk.Frame):
    """Creates a simple countdown timer

    The first 2/3 of the time is green.

    The first 2/3 of the remaining time is yellow.

    The remainder of the time is red.
    """
    def __init__(self, master):
        super().__init__(master)

        # create the widgets

        self.display = CountDownDisplay(self)
        # put the controls in a frame to control the spacing
        self.control_frame = tk.Frame(self)
        self.start_button = ttk.Button(self.control_frame, text='\u25b6', width=2)
        self.stop_button = ttk.Button(self.control_frame, text='\u25A0', width=2)
        self.pause_button = ttk.Button(self.control_frame, text='\u2016', width=2)
        self.set_button = ttk.Button(self, text='Set', command=self.set_timer)
        # layout the widgets
        self.display.grid(row=0, column=0)
        self.control_frame.grid(row=1, column=0, pady=(5, 10))
        self.start_button.grid(row=0, column=0)
        self.pause_button.grid(row=0, column=1)
        self.stop_button.grid(row=0, column=2)
        self.set_button.grid(row=2, column=0, pady=5)

        # add this frame to the parent layout
        self.grid(row=0, column=0)

    def reset(self):
        pass

    def set_timer(self):
        setup_window = tk.Toplevel(self.master)
        setup_window.title("Setup Timer")
        SimpleTimerSet(setup_window)


class MeetupTimer(tk.Frame):
    """Creates a meetup countdown timer

    This timer counts down to a certain date or a generic

    The first 3/4 of the time is green.

    The next 3/16 of the time is yellow.

    The last 3/64 of the time is red.
    """
    def __init__(self, master):
        super().__init__(master)

        # create the widgets
        self.display = CountDownDisplay(self)
        self.setup_button = ttk.Button(self, text='Set', command=self.set_timer)

        # add the widgets
        self.display.grid(row=0, column=0)
        self.setup_button.grid(row=1, column=0)

        self.grid(row=0, column=0)

    def reset(self):
        pass

    def set_timer(self):
        setup_window = tk.Toplevel(self.master)
        setup_window.title('Set Timer')
        MeetupTimerSet(setup_window)


class ControlFrame(ttk.Labelframe):
    """Controls which timer frame is displayed.

    There are two timer types:
        Simple timer - Counts down based on the user entered years, months, days, hours, minutes, seconds.

        Meetup timer - Counts down the time until the next occurrence of the meetup date

    The default is the simple timer
    """
    def __init__(self, master):
        super().__init__(master)

        self['text'] = 'Timer Type'

        # create the radio buttons

        self.timer_type_var = tk.StringVar()

        # make the simple timer the default
        self.timer_type_var.set('Simple')

        self.grid(row=1, column=0)

        self.timer_radio = ttk.Radiobutton(
            self,
            text="Simple",
            value="Simple",
            variable=self.timer_type_var,
            command=self.change_timer_type,
        )

        self.meetup_radio = ttk.Radiobutton(
            self,
            text="Meetup",
            value="Meetup",
            variable=self.timer_type_var,
            command=self.change_timer_type,
        )

        # add the radios to the parent
        self.timer_radio.grid(row=0, column=0, padx=5, pady=5)
        self.meetup_radio.grid(row=0, column=1, padx=5, pady=5)

        # store the two different timer type frames in a dictionary
        self.frames = {
            'Simple': SimpleTimer(master),
            'Meetup': MeetupTimer(master),
        }

        self.change_timer_type()

    def change_timer_type(self):
        for f in self.frames:
            if f == self.timer_type_var.get():
                frame = self.frames[self.timer_type_var.get()]
                frame.reset()
                frame.grid(row=0, column=0)
            else:
                self.frames[f].grid_remove()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Countdown Timer')
        self.resizable(False, False)


if __name__ == "__main__":
    app = App()
    ControlFrame(app)
    app.mainloop()
