from my_assistant import AppointmentAssistant
from my_tool import AppointmentLookup
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Robin, an appointment assistant.
Answer briefly and professionally.
The office is located at 40 Harbor Street, on the second floor.
Customers should bring a photo ID and last year's tax return to an appointment.
Only state facts that appear in these instructions.
If you do not know, say you do not know and tell the customer to ask the front desk."""

APPOINTMENTS = {
    "monday": ["9:00 am", "2:30 pm"],
    "wednesday": ["11:00 am", "3:00 pm"],
    "friday": ["10:00 am", "1:00 pm"],
}

tool = AppointmentLookup(APPOINTMENTS)
model = OllamaModel(MODEL_NAME)

assistant = AppointmentAssistant("Robin", tool, model, INSTRUCTIONS)

print("Type a message, or type quit to stop.")

user_message = input("You: ")

while user_message != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(assistant.history)}")
