import tkinter as tk
from tkinter import ttk

from tkcalendar import Calendar, DateEntry
import calendar
import datetime
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

    occurrences = {'First': 1, 'Second': 2, 'Third': 3, 'Fourth': 4, 'Fifth': 5, 'Teenth': 13, 'Last': 99}
    days_of_week = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6}

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
        """Calculate the next occurrence of meetup date
        :param year: The year to start looking for the next meetup
        :param month: The month to start looking for the next meetup
        :param week: The week of the meetup (first, second, third, fourth, fifth, teenth, last)
        teenth is the days from 13 - 19
        :param day_of_week: The weekday name
        """
        # occurrences = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'teenth': 13, 'last': 99}
        # days_of_week = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6}
        occurrence = MeetupDate.occurrences[week]
        week_day = MeetupDate.days_of_week[day_of_week]

        # find the last occurrence of the day of week
        if occurrence == 99:  # the last occurrence
            return MeetupDate.find_last_occurrence(year, month, week_day)

        if occurrence == 13:  # the teenth day
            return MeetupDate.find_teenth_occurrence(year, month, week_day)

        # the first through fifth occurrence
        return MeetupDate.find_nth_occurrence(year, month, week_day, occurrence)


# class DigitEntry(tk.Entry):
#     def __init__(self, master, **kw):
#         super().__init__(master, **kw)
#
#         vcmd = (self.register(self.validate), '%P')
#         ivcmd = (self.register(self.on_invalid), )
#         self['font'] = ('TkDefaultFont', 18)
#         self['validate'] = 'key'
#         self['validatecommand'] = vcmd
#         self['invalidcommand'] = ivcmd
#         self.set('')
#
#     def set(self, value):
#         """Set the value of the DigitEntry.
#
#         This is probably a bad idea for some reason
#         """
#         self.delete(0, tk.END)
#         self.insert(0, f'{value:02}')
#
#     def get(self):
#         """Gets the value of the DigitEtnry.
#
#         :return: the int value and 0 if empty
#         """
#         return int(super().get()) if super().get() else 0
#
#     @staticmethod
#     def validate(value):
#         if (value.strip().isdigit() and len(value) <= 2) or value == '':
#             return True
#         return False
#
#     def on_invalid(self):
#         self.bell()
#         self.bell()


class SimpleTimer(tk.Frame):
    """Creates a simple countdown timer"""
    def __init__(self, master):
        super().__init__(master)

        self.time_left = 0
        self.paused = False
        self.stopped = False
        self.running = False

        self.font_size = 24
        # create some validation variables
        vcmd = (self.register(self.validate), '%P')
        ivcmd = (self.register(self.on_invalid), '%P')

        # create our text variables
        self.hours_var = tk.StringVar()
        self.minutes_var = tk.StringVar()
        self.seconds_var = tk.StringVar()

        # create the widgets

        # self.display = CountDownDisplay(self, digits=2)
        self.display_frame = ttk.Frame(self)
        self.hours_entry = ttk.Entry(
            self.display_frame,
            width=2,
            textvariable=self.hours_var,
            validate='key',
            validatecommand=vcmd,
            invalidcommand=ivcmd,
            font=('TkDefaultFont', self.font_size),
        )
        self.minutes_entry = ttk.Entry(
            self.display_frame,
            width=2,
            textvariable=self.minutes_var,
            validate='key',
            validatecommand=vcmd,
            invalidcommand=ivcmd,
            font=('TkDefaultFont', self.font_size),
        )
        self.seconds_entry = ttk.Entry(
            self.display_frame,
            width=2,
            textvariable=self.seconds_var,
            validate='key',
            validatecommand=vcmd,
            invalidcommand=ivcmd,
            font=('TkDefaultFont', self.font_size),
        )

        # put the controls in a frame to control the spacing
        self.control_frame = tk.Frame(self)
        self.start_button = tk.Button(
            self.control_frame,
            text='\u25b6',
            width=2,
            font=('TkDefaultFont', self.font_size),
            command=self.timer_start,
        )
        self.stop_button = tk.Button(
            self.control_frame,
            text='\u25A0',
            width=2,
            font=('TkDefaultFont', self.font_size),
            command=self.timer_stop,
            state=tk.DISABLED,
        )
        self.pause_button = tk.Button(
            self.control_frame,
            text='\u2016',
            width=2,
            font=('TkDefaultFont', self.font_size),
            command=self.timer_pause,
            state=tk.DISABLED,
        )

        # layout the widgets

        # display frame
        self.hours_entry.grid(row=0, column=0, padx=5, pady=5)
        ttk.Separator(self.display_frame, orient='vertical').grid(row=0, column=1, sticky=(tk.N, tk.S), rowspan=2)
        self.minutes_entry.grid(row=0, column=2, pady=5, padx=5)
        ttk.Separator(self.display_frame, orient='vertical').grid(row=0, column=3, sticky="ns", rowspan=2)
        self.seconds_entry.grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(self.display_frame, text='H').grid(row=1, column=0)
        ttk.Label(self.display_frame, text='M').grid(row=1, column=2)
        ttk.Label(self.display_frame, text='S').grid(row=1, column=4)

        self.display_frame.grid(sticky='nswe')

        # control frame
        self.start_button.grid(row=0, column=0, sticky='s', pady=(10, 0))
        self.pause_button.grid(row=0, column=1, sticky='s')
        self.stop_button.grid(row=0, column=2, sticky='s')
        self.control_frame.grid()  # (row=1, column=0, pady=(5, 10))

        # add this frame to the parent layout
        # self.grid(row=0, column=0)
        self.rowconfigure(0, weight=2)
        self.clear_timer()

    def clear_timer(self):
        """Sets the hour, minutes, seconds entry widgets to empty strings"""
        self.hours_var.set('')
        self.minutes_var.set('')
        self.seconds_var.set('')

    def reset(self):
        """Resets the timer back to it's initial condition"""
        self.clear_timer()
        self.set_state(tk.NORMAL)
        self.running = False
        self.paused = False
        self.stopped = False
        self.time_left = 0
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def get_HMS(self):
        """Returns a tuple (hours, minutes, seconds)"""
        seconds = self.time_left
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds // 60
        seconds -= minutes * 60
        return hours, minutes, seconds

    def update_display(self, hours, minutes, seconds):
        """Updates the hours, minutes and seconds display

        :param hours: hours left to count down
        :param minutes: minutes left to count down
        :param seconds: seconds left to count down"""
        self.hours_var.set(hours)
        self.minutes_var.set(minutes)
        self.seconds_var.set(seconds)

    def tick(self):
        """Updates the time left, checks the stopped and paused flags, schedules the next call to tick"""
        if self.stopped:
            self.reset()
            return
        if not self.paused:
            if self.time_left > 0:
                self.time_left -= 1
            hours, minutes, seconds = self.get_HMS()
            self.update_display(hours, minutes, seconds)
        self.after(1000, self.tick)

    def timer_start(self):
        """Sets up the timer to run and starts the callback tick"""
        hours = int(self.hours_var.get()) if self.hours_var.get() else 0
        minutes = int(self.minutes_var.get()) if self.minutes_var.get() else 0
        seconds = int(self.seconds_var.get()) if self.seconds_var.get() else 0
        self.running = True
        self.set_state(tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.time_left = hours * 3600 + minutes * 60 + seconds
        self.tick()

    def timer_pause(self):
        """Toggles the paused flag"""
        self.paused = not self.paused

    def set_state(self, state):
        """Changes the state of the hour, minute, second entry widgets

        :param state: The state to put the h/m/s displays in

        VALID STATES
            TKINTER CONSTANTS
                NORMAL | DISABLED

            STRINGS
                'normal' | 'readonly'
        """
        self.hours_entry.config(state=state)
        self.minutes_entry.config(state=state)
        self.seconds_entry.config(state=state)

    def timer_stop(self):
        """Sets the stopped flag and disables the stop button"""
        self.stopped = True
        self.stop_button.config(state=tk.DISABLED)

    def validate(self, value):
        """Verifies that value is an integer in the range 0-99

        :param value: The value the widget will have if we return True"""
        # can only have 2 digits
        if len(value) > 2:
            return False
        # can only be digits
        for c in value:
            if not c.isdigit():
                return False
        return True

    def on_invalid(self, _):
        """Sounds the system bell"""
        self.bell()


class PlaceholderEntry(tk.Entry):
    """Entry widget which allows displaying simple text with default text in the widget."""
    def __init__(self, master=None, placeholdertext='Placeholder', placeholdercolor='gray', **kwargs):
        """Construct an placeholder entry widget with the parent MASTER.

         Includes placeholder text in the widget to give information to the user

        :
         Valid resource names: background, bd, bg, borderwidth, cursor,
         exportselection, fg, font, foreground, highlightbackground,
         highlightcolor, highlightthickness, insertbackground,
         insertborderwidth, insertofftime, insertontime, insertwidth,
         invalidcommand, invcmd, justify, relief, selectbackground,
         selectborderwidth, selectforeground, show, state, takefocus,
         textvariable, validate, validatecommand, vcmd, width,
         xscrollcommand, placeholdertext, placeholdercolor."""

        super().__init__(master, **kwargs)

        self.placeholdertext = placeholdertext
        self.placeholdercolor = placeholdercolor
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_place_holder()

    def put_place_holder(self):
        self['fg'] = self.placeholdercolor
        self.insert(0, self.placeholdertext)

    def focus_in(self, *args):
        if self['fg'] == self.placeholdercolor:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_place_holder()


# TODO: make this a modal window
class MeetupTimerSet(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        yvcmd = (self.register(self.validate_year), '%P')
        yivcmd = (self.register(self.on_invalid_year), '%P')

        mvcmd = (self.register(self.validate_month), '%P')
        mivcmd = (self.register(self.on_invalid_month), '%P')

        self.start_date = PlaceholderEntry(self, width=12, placeholdertext='mm/dd/yyyy',)
        hours = [str(x) for x in range(1, 13)]
        half_hours = []
        for hour, half in zip([hour + ':00' for hour in hours], [hour + ':30' for hour in hours]):
            half_hours.extend([hour, half])
        half_hours = half_hours[-2:] + half_hours[:len(half_hours)-2]
        combo_times = [x + ' AM' for x in half_hours] + [x + ' PM' for x in half_hours]
        self.start_time = ttk.Combobox(self, values=combo_times)
        self.start_time.current(0)
        self.pick_date = ttk.Button(self, text='Pick Date')

        self.start_date.grid(row=0, column=0)
        self.start_time.grid(row=1, column=0)
        self.pick_date.grid(row=0, column=1)

        self.pack()

    def validate_year(self, value):
        if (value.strip().isdigit() and len(value) <= 4) or value == '':
            return True
        return False

    def on_invalid(self):
        self.master.Beep()
        self.master.Beep()

    def on_invalid_year(self):
        pass

    def validate_month(self, v):
        return True

    def on_invalid_month(self):
        pass


class MeetupTimer(tk.Frame):
    """Creates a meetup countdown timer
    """
    def __init__(self, master):
        super().__init__(master)
        self.font_size = 24
        self.years_var = tk.StringVar(value='')
        self.months_var = tk.StringVar(value='')
        self.days_var = tk.StringVar(value='')
        self.hours_var = tk.StringVar(value='')
        self.minutes_var = tk.StringVar(value='')
        self.seconds_var = tk.StringVar(value='')

        # create the widgets
        # self.display = CountDownDisplay(self, ymd=True, digits=2)
        ttk.Entry(
            self,
            state='readonly',
            textvariable=self.years_var,
            font=('TkDefaultFont', self.font_size),
            width=2,
        ).grid(column=0, row=0, padx=5, pady=5)  # years
        ttk.Separator(self, orient='vertical', ).grid(column=1, row=0, rowspan=2, sticky='ns')
        ttk.Entry(
            self,
            state='readonly',
            textvariable=self.months_var,
            font=('TkDefaultFont', self.font_size),
            width=2
        ).grid(column=2, row=0, padx=5, pady=5)  # months
        ttk.Separator(self, orient='vertical').grid(column=3, row=0, rowspan=2, sticky='ns')
        ttk.Entry(
            self,
            state='readonly',
            textvariable=self.days_var,
            font=('TkDefaultFont', self.font_size),
            width=2
        ).grid(column=4, row=0, padx=5, pady=5)  # days

        ttk.Entry(
            self,
            state='readonly',
            textvariable=self.hours_var,
            font=('TkDefaultFont', self.font_size),
            width=2
        ).grid(column=0, row=2, padx=5, pady=5)  # years
        ttk.Separator( self, orient='vertical', ).grid(column=1, row=2, rowspan=2, sticky='ns')
        ttk.Entry(
            self,
            state='readonly',
            textvariable=self.minutes_var,
            font=('TkDefaultFont', self.font_size),
            width=2,
        ).grid(column=2, row=2)  # months
        ttk.Separator(self, orient='vertical').grid(column=3, row=2, rowspan=2, sticky='ns')
        ttk.Entry(
            self,
            state='readonly',
            textvariable=self.seconds_var,
            font=('TkDefaultFont', self.font_size),
            width=2,
        ).grid(column=4, row=2, padx=5, pady=5)  # days

        ttk.Label(self, text='H').grid(column=0, row=3)
        ttk.Label(self, text='M').grid(column=2, row=3)
        ttk.Label(self, text='S').grid(column=4, row=3)

        ttk.Label(self, text='Y').grid(column=0, row=1)
        ttk.Label(self, text='M').grid(column=2, row=1)
        ttk.Label(self, text='D').grid(column=4, row=1)

        self.setup_button = ttk.Button(self, text='Set', command=self.set_timer)

        # add the widgets
        self.setup_button.grid(row=4, column=0, columnspan=5)

        # self.grid(row=0, column=0)

    def reset(self):
        pass

    def set_timer(self):
        setup_window = tk.Toplevel(self.master)
        setup_window.title('Set Timer')
        MeetupTimerSet(setup_window)
        print('hello')


class View(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(0, weight=2)
        self.columnconfigure(0, weight=2)

        self.notebook = ttk.Notebook(self)
        simple_timer = SimpleTimer(self.notebook)
        meetup_timer = MeetupTimer(self.notebook)
        simple_timer.grid(row=0, column=0, sticky=tk.NSEW)
        meetup_timer.grid(sticky=tk.NSEW)
        self.notebook.rowconfigure(0, weight=1)
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.add(simple_timer, text='Timer')
        self.notebook.add(meetup_timer, text='Meetup')
        self['background'] = 'blue'
        self.notebook.grid(sticky=tk.NSEW)

        self.grid(padx=10, pady=10, sticky=tk.NSEW)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Countdown Timer')

        view = View(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
