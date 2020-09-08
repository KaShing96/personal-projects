# === Console printing class ===
class Console(): 
    """
    A class to handle console messages.
    """
    def __init__(self, tags=True):
        """
        Constructor class. Instantiates the tags.
        """
        # Instantiate tags
        self.running, self.success_message, self.failure_message = ("", "", "")

        if tags: 
            # Enable tags
            self.running_message = "[RUNNING]"
            self.success_message = "[SUCCESS]"
            self.failure_message = "[FAILED]"

    
    def start(self, s):
        """
        Prints s to the console. The default is 'Running'.
        """
        self.task = s

        print(f"{self.running_message} {s}", end="\r")


    def success(self):
        """
        Edits the current line to a success of the current message.
        """
        print(f"{self.success_message} {self.task}")


    def failure(self, e=None): 
        """
        Edits the current line to a failure of the current message. 

        Raises an optional error, e.
        """
        print(f"{self.failure_message} {self.task}")

        if e: 
            raise e