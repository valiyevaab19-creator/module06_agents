HANDOFF_WORDS = ["book", "cancel", "reschedule"]
MAX_TOOL_ROUNDS = 3


class AppointmentAssistant:
    """An appointment assistant that supports both rules and model-chosen tools."""

    def __init__(self, name, tools, model=None, instructions=""):
        self.name = name
        self.tools = tools
        self.model = model
        self.instructions = instructions
        self.history = []

    def respond(self, user_message):
        """Record the user message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Use Week 12 tools when available, otherwise keep Week 11 behavior."""
        text = user_message.lower()

        if hasattr(self.tools, "tool_list"):
            if "cancel" in text or "reschedule" in text:
                return "I can't change a booking. I'm passing you to the front desk."
            return self.model_reply()

        for word in HANDOFF_WORDS:
            if word in text:
                return "I can't change the schedule. I'm passing you to the front desk."

        if "hello" in text:
            return f"Hello! I'm {self.name}. Ask me which times are open on a day."

        day = self.tools.find_day(user_message)

        if day is not None:
            times = self.tools.times_for(day)
            return f"Open times on {day}: {', '.join(times)}."

        if "available" in text or "open" in text:
            return "Which day? I can check Monday, Wednesday, or Friday."

        return self.legacy_model_reply()

    def legacy_model_reply(self):
        """Use the Week 11 model interface."""
        if self.model is None:
            return "I'm not sure how to help with that. I can list open times."

        reply = self.model.reply(self.instructions, self.history)

        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."

        return reply

    def model_reply(self):
        """Ask the model, run checked tools, and ask again up to a limit."""
        rounds = 0

        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()
            decision = self.model.decide(
                self.instructions,
                self.history,
                tool_list,
            )

            if decision is None:
                return "Sorry, I can't answer that right now. Please try again in a moment."

            if "text" in decision:
                return decision["text"]

            name = decision["tool"]
            arguments = decision["arguments"]
            result = self.tools.run(name, arguments, self.history)

            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )

            rounds += 1

        return "Sorry, I couldn't finish that. I'm passing you to the front desk."
