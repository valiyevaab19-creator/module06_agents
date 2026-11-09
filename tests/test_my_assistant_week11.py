from unittest.mock import Mock

from mock_model import MockModel
from my_assistant import AppointmentAssistant
from my_tool import AppointmentLookup


def make_tool():
    return AppointmentLookup(
        {
            "monday": ["9:00 am", "2:30 pm"],
            "wednesday": ["11:00 am", "3:00 pm"],
            "friday": ["10:00 am", "1:00 pm"],
        }
    )


def test_model_handles_other_questions():
    assistant = AppointmentAssistant("Robin", make_tool(), MockModel(), "Be helpful.")
    assert "not sure" in assistant.respond("What should I bring?").lower()


def test_safe_reply_when_model_returns_none():
    silent_model = Mock()
    silent_model.reply.return_value = None

    assistant = AppointmentAssistant("Robin", make_tool(), silent_model, "Be helpful.")

    assert "try again" in assistant.respond("What should I bring?").lower()


def test_schedule_rule_works_without_model_answer():
    silent_model = Mock()
    silent_model.reply.return_value = None

    assistant = AppointmentAssistant("Robin", make_tool(), silent_model, "Be helpful.")

    assert "9:00 am" in assistant.respond("What times are open on Monday?")
