class BookingQueue:
    """Bookings waiting for front desk approval."""

    def __init__(self):
        self.requests = []
        self.bookings = []

    def request_booking(self, name, day, time):
        """Ask the front desk to book an appointment.

        Args:
            name: The client's full name.
            day: The appointment day, like monday.
            time: The appointment time, like 9:00 am.
        """
        number = len(self.requests) + 1
        request = {
            "number": number,
            "name": name,
            "day": day.lower(),
            "time": time.lower(),
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to the front desk for approval."

    def waiting(self):
        return [r for r in self.requests if r["status"] == "waiting"]

    def find(self, number):
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.bookings.append(request.copy())
        return f"Request {number} approved."

    def reject(self, number):
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
