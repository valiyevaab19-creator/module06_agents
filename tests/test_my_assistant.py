from booking_queue import BookingQueue
from fake_model import FakeModel
from my_assistant import AppointmentAssistant
from my_tool import AppointmentLookup
from my_toolbox import AppointmentToolbox


def make_assistant(model):
    appointments = {
        "monday": ["9:00 am", "2:30 pm"],
        "wednesday": ["11:00 am", "3:00 pm"],
        "friday": ["10:00 am", "1:00 pm"],
    }

    appointment_tool = AppointmentLookup(appointments)
    booking_queue = BookingQueue()
    tools = AppointmentToolbox(appointment_tool, booking_queue)

    assistant = AppointmentAssistant(
        "Robin",
        tools,
        model,
        "Be brief and professional.",
    )

    return assistant, booking_queue


def ask_for_tool(name, arguments):
    return {"tool": name, "arguments": arguments}


def test_made_up_name_is_refused():
    model = FakeModel(
        [
            ask_for_tool(
                "request_booking",
                {
                    "name": "Dana Cruz",
                    "day": "monday",
                    "time": "9:00 am",
                },
            ),
            {"text": "What is your full name?"},
        ]
    )

    assistant, queue = make_assistant(model)
    assistant.respond("Please book Monday at 9:00 am")

    assert "has not given that name" in assistant.history[1]["content"]
    assert queue.waiting() == []


def test_booking_waits_for_approval():
    model = FakeModel(
        [
            ask_for_tool(
                "request_booking",
                {
                    "name": "Dana Cruz",
                    "day": "monday",
                    "time": "9:00 am",
                },
            ),
            {"text": "Sent to the front desk."},
        ]
    )

    assistant, queue = make_assistant(model)
    assistant.respond("My name is Dana Cruz. Please book Monday at 9:00 am")

    assert len(queue.waiting()) == 1
    assert len(queue.bookings) == 0


def test_cancel_goes_to_front_desk():
    assistant, queue = make_assistant(FakeModel([]))

    reply = assistant.respond("Please cancel my appointment")

    assert "front desk" in reply
    assert queue.waiting() == []


def test_model_can_check_open_times():
    model = FakeModel(
        [
            ask_for_tool("check_open_times", {"day": "monday"}),
            {"text": "Monday has 9:00 am and 2:30 pm open."},
        ]
    )

    assistant, queue = make_assistant(model)
    assistant.respond("What times are open on Monday?")

    assert "9:00 am" in assistant.history[1]["content"]
    assert queue.waiting() == []
