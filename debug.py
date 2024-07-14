import time
import os

class Debug:
    @staticmethod
    def pause_and_clear(duration=1):
        """
        Pause for the specified duration and then clear the terminal window.

        :param duration: The duration to pause in seconds.
        """
        time.sleep(duration)

        # Clear the terminal
        os.system("cls" if os.name == "nt" else "clear")