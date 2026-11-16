from booking_queue import BookingQueue
from my_assistant import AppointmentAssistant
from my_tool import AppointmentLookup
from my_toolbox import AppointmentToolbox
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Robin, an appointment assistant.
Answer briefly and professionally.
The office is located at 40 Harbor Street, on the second floor.
Customers should bring a photo ID and last year's tax return to an appointment.
Only state facts that appear in these instructions or in tool results.
If the client only says hello, greet them and ask how you can help.
If you do not know, say you do not know and tell the customer to ask the front desk."""

APPOINTMENTS = {
    "monday": ["9:00 am", "2:30 pm"],
    "wednesday": ["11:00 am", "3:00 pm"],
    "friday": ["10:00 am", "1:00 pm"],
}

appointment_tool = AppointmentLookup(APPOINTMENTS)
booking_queue = BookingQueue()
tools = AppointmentToolbox(appointment_tool, booking_queue)
model = OllamaModel(MODEL_NAME)

assistant = AppointmentAssistant(
    "Robin",
    tools,
    model,
    INSTRUCTIONS,
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")

while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(assistant.history)}")

print("Front desk review")

for request in booking_queue.waiting():
    number = request["number"]
    print(f"Request {number}: {request['name']}, {request['day']} {request['time']}")

    answer = input("Approve? yes or no: ")

    if answer == "yes":
        print(booking_queue.approve(number))
    else:
        print(booking_queue.reject(number))

print(f"Bookings: {len(booking_queue.bookings)}")
