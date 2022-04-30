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


class TimerDisplay(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master)
        self.years_label = tk.Label(self, text="00", **kw)
        self.months_label = tk.Label(self, text="00", **kw)
        self.days_label = tk.Label(self, text="00", **kw)
        self.hours_label = tk.Label(self, text="00", **kw)
        self.minutes_label = tk.Label(self, text="00", **kw)
        self.seconds_label = tk.Label(self, text="00", **kw)

        self.years_label.grid(row=1, column=0, padx=5, pady=(5, 0))
        self.months_label.grid(row=1, column=1, padx=5, pady=(5, 0))
        self.days_label.grid(row=1, column=2, padx=5, pady=(5, 0))

        tk.Label(self, text='Y').grid(row=2, column=0)
        tk.Label(self, text='M').grid(row=2, column=1)
        tk.Label(self, text='D').grid(row=2, column=2)

        self.hours_label.grid(row=3, column=0, padx=5, pady=(5, 0))
        self.minutes_label.grid(row=3, column=1, padx=5, pady=(5, 0))
        self.seconds_label.grid(row=3, column=2, padx=5, pady=(5, 0))

        tk.Label(self, text='H').grid(row=4, column=0)
        tk.Label(self, text='M').grid(row=4, column=1)
        tk.Label(self, text='S').grid(row=4, column=2)


class ButtonFrame(ttk.Frame):
    def __init__(self, master):
        super(ButtonFrame, self).__init__(master=master)
        self.start_button = ttk.Button(self, text='Start')
        self.stop_button = ttk.Button(self, text='Stop')
        self.reset_button = ttk.Button(self, text='Reset')
        self.pause_button = ttk.Button(self, text='Pause')
        self.start_button.grid(row=2, column=0)
        self.stop_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2)
        self.pause_button.grid(row=2, column=3)


class RadioButtons(ttk.Frame):
    def __init__(self, master):
        super(RadioButtons, self).__init__(master=master)
        self.timed_radio = ttk.Radiobutton(self, text="Timer", value="timer")
        self.meetup_radio = ttk.Radiobutton(self, text="Meetup", value="meetup")
        self.timed_radio.grid(row=0, column=0)
        self.meetup_radio.grid(row=0, column=1)


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # create the radio buttons to choose between a date in the future or a set amount of time
        self.radio_buttons = RadioButtons(self)
        self.timer_display = TimerDisplay(self, background='black', foreground='green', font=('Lucida Console', 12))
        self.buttons = ButtonFrame(self)

        # add widgets to the view

        self.radio_buttons.grid(row=0, column=0)
        self.timer_display.grid(row=1, column=0, columnspan=2)
        self.buttons.grid(row=2, column=0)


class Model:
    def __init__(self):
        self.timed = False
        self.meetup = False
        self.timer_type = tk.StringVar()


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.setup_view()
        self.setup_event_handlers()
        self.setup_commands()

    def setup_view(self):
        self.view.radio_buttons.meetup_radio['variable'] = self.model.timer_type
        self.view.radio_buttons.timed_radio['variable'] = self.model.timer_type

    def setup_event_handlers(self):
        pass

    def setup_commands(self):
        self.view.radio_buttons.meetup_radio['command'] = self.timer_type_changed
        self.view.radio_buttons.timed_radio['command'] = self.timer_type_changed

    def timer_type_changed(self):
        if self.model.timer_type.get() == 'meetup':
            self.view.buttons.pause_button['state'] = tk.DISABLED
        else:
            self.view.buttons.pause_button['state'] = tk.NORMAL


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title = "Count Down"

        model = Model()

        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        controller = Controller(model, view)


if __name__ == "__main__":
    app = App()
    app.mainloop()
