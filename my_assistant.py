HANDOFF_WORDS = ["book", "cancel", "reschedule"]


class AppointmentAssistant:
    """A mock assistant that checks available appointment times."""

    def __init__(self, name, tool):
        # Store the assistant name and lookup tool.
        self.name = name
        self.tool = tool
        self.history = []

    def respond(self, user_message):
        # Record the user message.
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        # Record the assistant reply.
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        text = user_message.lower()

        for word in HANDOFF_WORDS:
            if word in text:
                return "I can't change the schedule. I'm passing you to the front desk."

        if "hello" in text:
            return f"Hello! I'm {self.name}. Ask me which times are open on a day."

        day = self.tool.find_day(user_message)

        if day is not None:
            times = self.tool.times_for(day)
            return f"Open times on {day}: {' and '.join(times)}."

        if "available" in text or "open" in text:
            return "Which day? I can check Monday, Wednesday, or Friday."

        return "I'm not sure how to help with that. I can list open times."
