HANDOFF_WORDS = ["book", "cancel", "reschedule"]


class AppointmentAssistant:
    """An appointment assistant that uses rules first and a model for everything else."""

    def __init__(self, name, tool, model=None, instructions=""):
        # Store the assistant name so it can identify itself.
        self.name = name
        # Store the appointment lookup tool so schedule facts stay in code.
        self.tool = tool
        # Store the model so unknown questions can be sent to it.
        self.model = model
        # Store instructions so the model receives verified business facts.
        self.instructions = instructions
        # Keep the conversation history so the model can see earlier messages.
        self.history = []

    def respond(self, user_message):
        """Record the user message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Use schedule rules first. Otherwise ask the model."""
        text = user_message.lower()

        for word in HANDOFF_WORDS:
            if word in text:
                return "I can't change the schedule. I'm passing you to the front desk."

        if "hello" in text:
            return f"Hello! I'm {self.name}. Ask me which times are open on a day."

        day = self.tool.find_day(user_message)

        if day is not None:
            times = self.tool.times_for(day)
            return f"Open times on {day}: {', '.join(times)}."

        if "available" in text or "open" in text:
            return "Which day? I can check Monday, Wednesday, or Friday."

        return self.model_reply()

    def model_reply(self):
        """Ask the model when no rule applies and use a safe reply if it fails."""
        if self.model is None:
            return "I'm not sure how to help with that. I can list open times."

        reply = self.model.reply(self.instructions, self.history)

        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."

        return reply
