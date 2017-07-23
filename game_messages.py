import textwrap

import libtcodpy as libtcod


class Message:
    def __init__(self, text, color=libtcod.white):
        """
        Create a new Message
        :param str text: Message text
        :param libtcod.color color: Text Color
        """
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        """
        Add a message to the message log
        :param Message message:
        """
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for a new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object with the text and color of the original
            self.messages.append(Message(line, message.color))
