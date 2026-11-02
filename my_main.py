from my_assistant import AppointmentAssistant
from my_tool import AppointmentLookup

APPOINTMENTS = {
    "monday": ["9:00 am", "2:30 pm"],
    "wednesday": ["11:00 am", "3:00 pm"],
    "friday": ["10:00 am", "1:00 pm"],
}

tool = AppointmentLookup(APPOINTMENTS)
assistant = AppointmentAssistant("Robin", tool)

print("Type a message, or type quit to stop.")

user_message = input("You: ")

while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(assistant.history)}")
