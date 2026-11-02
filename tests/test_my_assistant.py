from my_assistant import AppointmentAssistant
from my_tool import AppointmentLookup


def make_assistant():
    appointments = {
        "monday": ["9:00 am", "2:30 pm"],
        "wednesday": ["11:00 am"],
        "friday": ["10:00 am"],
    }
    return AppointmentAssistant("Robin", AppointmentLookup(appointments))


def test_known_day_uses_tool():
    assistant = make_assistant()
    assert "9:00 am" in assistant.respond("What is open on Monday?")


def test_missing_day_gets_helpful_reply():
    assistant = make_assistant()
    assert "Which day" in assistant.respond("What is available?")


def test_booking_goes_to_person():
    assistant = make_assistant()
    assert "front desk" in assistant.respond("Please book me for Monday")


def test_unknown_request_gets_safe_reply():
    assistant = make_assistant()
    assert "not sure" in assistant.respond("Do you validate parking?")


def test_history_records_both_messages():
    assistant = make_assistant()
    assistant.respond("hello")
    assert len(assistant.history) == 2
