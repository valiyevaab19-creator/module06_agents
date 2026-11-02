class AppointmentLookup:
    """A tool that stores available appointment times."""

    def __init__(self, appointments):
        # Store the appointment schedule.
        self.appointments = appointments

    def find_day(self, text):
        # Find a known day in the user's message.
        for day in self.appointments:
            if day.lower() in text.lower():
                return day
        return None

    def times_for(self, day):
        # Return times for a known day.
        if day in self.appointments:
            return self.appointments[day]
        return None
