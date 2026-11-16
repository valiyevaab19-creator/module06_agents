class AppointmentToolbox:
    """Check every tool request before it runs."""

    def __init__(self, appointment_tool, booking_queue):
        self.appointment_tool = appointment_tool
        self.booking_queue = booking_queue

    def tool_list(self):
        return [
            self.appointment_tool.check_open_times,
            self.booking_queue.request_booking,
        ]

    def run(self, name, arguments, history):
        if name == "check_open_times":
            day = self.clean(arguments, "day")
            if day == "":
                return "The day is missing. Ask the client which day."
            if not self.customer_said(history, day):
                return "The client has not given that day. Ask them for it."
            return self.appointment_tool.check_open_times(day)

        if name == "request_booking":
            client = self.clean(arguments, "name")
            day = self.clean(arguments, "day")
            time = self.clean(arguments, "time")

            if client == "" or day == "" or time == "":
                return "The client's name, day, and time are all needed."

            if not self.customer_said(history, client):
                return "The client has not given that name. Ask them for it."
            if not self.customer_said(history, day):
                return "The client has not given that day. Ask them for it."
            if not self.customer_said(history, time):
                return "The client has not given that time. Ask them for it."

            return self.booking_queue.request_booking(client, day, time)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
