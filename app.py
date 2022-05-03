import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import calendar
from datetime import date
from typing import Any

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


# TODO: make this a modal window
class MeetupTimerSet(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        tk.Label(self, text="Hello from the meetup timer setup").pack()

        self.pack()


class DigitEntry(tk.Entry):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        vcmd = (self.register(self.validate), '%P')
        ivcmd = (self.register(self.on_invalid), )
        self['font'] = ('TkDefaultFont', 18)
        self['validate'] = 'key'
        self['validatecommand'] = vcmd
        self['invalidcommand'] = ivcmd
        self.set('')

    def set(self, value):
        """Set the value of the DigitEntry.

        This is probably a bad idea for some reason
        """
        self.delete(0, tk.END)
        self.insert(0, str(value))

    def get(self):
        """Gets the value of the DigitEtnry.

        :return: the int value and 0 if empty
        """
        return int(super().get()) if super().get() else 0

    @staticmethod
    def validate(value):
        if (value.strip().isdigit() and len(value) <= 2) or value == '':
            return True
        return False

    def on_invalid(self):
        self.bell()
        self.bell()


class CountDownDisplay(tk.Frame):
    """Frame widget which may contain other widgets.

        STANDARD OPTIONS
            background, bd, bg, borderwidth,
            class , colormap, container, cursor, height, highlightbackground,
            highlightcolor, highlightthickness, relief, takefocus, visual, width.
        WIDGET SPECIFIC OPTIONS
            ymd - include the TMD displys
            digits - the number of digits per display field
        """
    def __init__(self, master, ymd=False, digits=None, **kwargs):
        super().__init__(master, **kwargs)
        self.ymd = ymd
        self.digits = digits

        # create the widgets
        if self.ymd:
            self.years_entry = DigitEntry(self, width=self.digits)  # DigitLabel(self)
            self.months_entry = DigitEntry(self, width=self.digits)
            self.days_entry = DigitEntry(self, width=self.digits)

        self.hours_entry = DigitEntry(self, width=self.digits)
        self.minutes_entry = DigitEntry(self, width=self.digits)
        self.seconds_entry = DigitEntry(self, width=self.digits)

        # add the widgets
        if self.ymd:
            # years, months, days
            self.years_entry.grid(row=0, column=0, padx=5, pady=(5, 0))
            tk.Label(self, text='|').grid(row=0, column=1, pady=(3, 0))
            self.months_entry.grid(row=0, column=2, padx=5, pady=(5, 0))
            tk.Label(self, text='|').grid(row=0, column=3, pady=(3, 0))
            self.days_entry.grid(row=0, column=4, padx=5, pady=(5, 0))

            tk.Label(self, text='Y').grid(row=1, column=0)
            tk.Label(self, text='M').grid(row=1, column=2)
            tk.Label(self, text='D').grid(row=1, column=4)

        # hours, minutes, seconds
        self.hours_entry.grid(row=2, column=0, padx=5, pady=(5, 0))
        tk.Label(self, text='|').grid(row=2, column=1, pady=(3, 0))
        self.minutes_entry.grid(row=2, column=2, padx=5, pady=(5, 0))
        tk.Label(self, text='|').grid(row=2, column=3, pady=(3, 0))
        self.seconds_entry.grid(row=2, column=4, padx=5, pady=(5, 0))

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

        self.display = CountDownDisplay(self, digits=2)
        # put the controls in a frame to control the spacing
        self.control_frame = tk.Frame(self)
        self.start_button = ttk.Button(self.control_frame, text='\u25b6', width=2)
        self.stop_button = ttk.Button(self.control_frame, text='\u25A0', width=2)
        self.pause_button = ttk.Button(self.control_frame, text='\u2016', width=2)
        # layout the widgets
        self.display.grid(row=0, column=0)
        self.control_frame.grid(row=1, column=0, pady=(5, 10))
        self.start_button.grid(row=0, column=0)
        self.pause_button.grid(row=0, column=1)
        self.stop_button.grid(row=0, column=2)

        # add this frame to the parent layout
        self.grid(row=0, column=0)

    def reset(self):
        pass


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
        self.display = CountDownDisplay(self, ymd=True, digits=2)
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
        print('hello')


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
        )

        self.meetup_radio = ttk.Radiobutton(
            self,
            text="Meetup",
            value="Meetup",
            variable=self.timer_type_var,
        )

        # add the radios to the parent
        self.timer_radio.grid(row=0, column=0, padx=5, pady=5)
        self.meetup_radio.grid(row=0, column=1, padx=5, pady=5)


class Model:
    def __init__(self):
        super().__init__()
        self.meetup_years = 0
        self.meetup_months = 0
        self.meetup_days = 0
        self.meetup_hours = 0
        self.meetup_minutes = 0
        self.meetup_seconds = 0
        self.meetup_hundredths = 0
        self.simple_hours = 0
        self.simple_minutes = 0
        self.simple_seconds = 0
        self.simple_hundredths = 0
        self.simple_paused = False
        self.simple_timer_first_run = True



class View(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frames = {
            'Simple': SimpleTimer(self),
            'Meetup': MeetupTimer(self),
        }
        self.timer_type = ControlFrame(self)

        self.frames['Simple'].grid(row=0, column=0)
        self.timer_type.grid(row=1, column=0)
        self.pack()


class Controller:
    def __init__(self, master, model, view):
        super().__init__()
        self.master = master
        self.model = model
        self.view = view
        self.set_command_handlers()

        self.change_timer_type()

    def set_command_handlers(self):
        self.view.timer_type.timer_radio['command'] = self.change_timer_type
        self.view.timer_type.meetup_radio['command'] = self.change_timer_type
        self.view.frames['Simple'].start_button['command'] = self.simple_timer_start
        self.view.frames['Simple'].pause_button['command'] = self.simple_timer_pause
        self.view.frames['Simple'].stop_button['command'] = self.simple_timer_stop

    def change_timer_type(self):
        for f in self.view.frames:
            if f == self.view.timer_type.timer_type_var.get():
                frame = self.view.frames[self.view.timer_type.timer_type_var.get()]
                frame.reset()
                frame.grid(row=0, column=0)
            else:
                self.view.frames[f].grid_remove()

    def simple_timer_start(self):
        self.model.simple_hours = self.view.frames['Simple'].display.hours_entry.get()
        self.model.simple_minutes = self.view.frames['Simple'].display.minutes_entry.get()
        self.model.simple_seconds = self.view.frames['Simple'].display.seconds_entry.get()
        self.model.simple_timer_running = True
        self.model.simple_timer_paused = False
        self.model.simple_timer_first_run = True
        self.simple_timer_run()

    def simple_timer_pause(self):
        self.model.simple_paused = not self.model.simple_paused

    def simple_timer_stop(self):
        # reset the display to all 0's
        # make all displays editable
        self.model.simple_timer_running = False
        self.view.frames['Simple'].display.hours_entry.set('')
        self.view.frames['Simple'].display.minutes_entry.set('')
        self.view.frames['Simple'].display.seconds_entry.set('')

        self.view.frames['Simple'].display.hours_entry['state'] = 'normal'
        self.view.frames['Simple'].display.minutes_entry['state'] = 'normal'
        self.view.frames['Simple'].display.seconds_entry['state'] = 'normal'

    def simple_timer_run(self):
        print(self.model.simple_hours, self.model.simple_minutes, self.model.simple_seconds, self.model.simple_hundredths)
        if not self.model.simple_timer_running:
            return
        if self.model.simple_paused:
            self.master.after(1000, self.simple_timer_run)
            return
        if self.model.simple_seconds > 1:
            self.model.simple_seconds -= 1
        elif self.model.simple_minutes > 0:
            self.model.simple_minutes -= 1
            self.model.simple_seconds = 59
        elif self.model.simple_hours > 0:
            self.model.simple_hours -= 1
            self.model.simple_minutes = 59
            self.model.simple_seconds = 59
        else:
            if self.model.simple_timer_running:
                self.model.simple_seconds = 0
                self.update_simple_display()
                self.master.update()
                self.view.bell()
                return
        self.update_simple_display()
        if self.model.simple_timer_running:
            self.master.after(1000, self.simple_timer_run)

    def update_simple_display(self):
        self.view.frames['Simple'].display.hours_entry.set(self.model.simple_hours)
        self.view.frames['Simple'].display.minutes_entry.set(self.model.simple_minutes)
        self.view.frames['Simple'].display.seconds_entry.set(self.model.simple_seconds)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Countdown Timer')
        self.resizable(False, False)

        view = View(self)
        model = Model()

        Controller(self, model, view)


if __name__ == "__main__":
    app = App()
    app.mainloop()
