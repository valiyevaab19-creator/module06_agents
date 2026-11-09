# echo_model.py
# Author: Aigerim Valiyeva


class EchoModel:
    """A model that repeats the user's last message."""

    def reply(self, instructions, history):
        # history[-1] gets the newest conversation message so the model can echo it.
        last_message = history[-1]["content"]
        # Return the required prefix plus exactly what the user last said.
        return "You said: " + last_message
