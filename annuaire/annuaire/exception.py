"""Module exceptions."""


class AnnuaireException(Exception):
    """Class AnnuaireException."""

    message = None

    def __init__(self, message):
        """
        Constructor.

        :param message:
        """
        self.message = message
