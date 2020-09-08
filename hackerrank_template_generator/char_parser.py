# === Parser Class ===
import string 

class Parser():
    """
    A parser class to ensure all words are printables. This does not include tokens.
    """
    def __init__(self, printables=None):
        """
        Constructs the list of printables.
        """
        self.printables = printables if printables else set(string.printable)


    def parse(self, s, wild=" "): 
        """
        Returns a string that is parsed. All non-printables are replaced with wild.

        Params
        ======
        s: str
            The string to be checked
        wild: str
            The character to be replaced in case of a non-printable.

        Returns
        =======
        new_string: str
            Parsed string
        """
        new_string = ""

        for i in s: 
            new_string += i if i in self.printables else wild

        return new_string