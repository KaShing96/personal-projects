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


# === WebDriver Class ===
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
from selenium.webdriver.remote.remote_connection import LOGGER

class Driver():
    """
    A class to handle the webdriver.
    """
    def __init__(self, gecko=None, link=None):
        """
        Constructor class. Starts the webdriver from the given executable path 'gecko' and optionally goes to the required link.

        The function automatically searches parent folders for gecko if it is None.

        Params
        ======
        gecko: str
            Path to the geckodriver
        link: str
            Optional link to move to
        """
        # Verify geckodriver is available
        if not gecko:

            # Search for driver
            driver_name = "geckodriver.exe"
            
            # Start with current directory and move up
            cd = Path().cwd()

            while True: 
                contents = [str(x.name) for x in cd.iterdir()]

                if driver_name not in contents:
                    cd = cd.parent 

                else: 
                    for i in cd.iterdir():
                        if driver_name == i.name: 
                            gecko = i 

                    break 

        # Disable logging
        LOGGER.setLevel(logging.WARNING)

        # Options
        o = Options()
        o.add_argument("--headless") 

        # Start driver
        self.d = webdriver.Firefox(executable_path=gecko, options=o)

        # Move to link
        if link: 
            self.goto(link)
        

    def goto(self, link): 
        """
        Goes to the given link.
        """
        self.d.get(link)


    def source(self):
        """
        Returns page source

        Returns
        =======
        _: str
            The page source HTML. 
        """
        return self.d.page_source

    
    def wait(self, method, s, wait_time=10):
        """
        Waits via the given method, checking for s, for the given wait time.

        Params
        ======
        method: By
            The method to use to wait, e.g. By.ID, By.CLASS_NAME, etc.
        s: str
            The string to check for, using the given method. Refer to selenium WebDriverWait. 
        wait_time: int
            The time in seconds to wait.

        Returns
        =======
        _: WebElement
            The WebElement we wait for
        """
        return WebDriverWait(self.d, wait_time).until(EC.presence_of_element_located((method, s)))


    def close(self):
        """
        Closes the driver.
        """
        self.d.close()


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


# === FolderWriter Class ===
from pathlib import Path

class FolderWriter():
    """
    Handle writing to the new folder.
    """
    def __init__(self, dest, title, link, imports, function, main, inputs, outputs):
        self.dest = dest 
        self.title = title
        self.link = link
        self.imports = imports
        self.function = function
        self.main = main
        self.inputs = inputs
        self.outputs = outputs


    def write(self):
        """
        Writes to files in the new desired folder.
        """
        # Identify parent folder
        parent = Path(self.dest)
        parent = parent.resolve(strict=True)

        # Create folder
        target_folder = parent / self.title.lower().replace(" ", "_")
        target_folder = target_folder
        target_folder.exists() or target_folder.mkdir()

        # Create README
        README_path = target_folder / "README.md"
        README_path.exists() or README_path.touch()
        
        rw = READMEWriter(README_path, self.title, self.link)
        rw.write()

        # Create test_functions.py
        tf_path = target_folder / "test_functions.py"
        tf_path.exists() or tf_path.touch()

        tfw = TestFunctionWriter(tf_path)
        tfw.write()

        # Create functions.py
        f_path = target_folder / "functions.py"
        f_path.exists() or f_path.touch()

        fw = FunctionWriter(f_path, self.imports, self.function, self.main)
        fw.write()

        # Create test case folder and write test cases
        tc_path = target_folder / "test_cases"
        tc_path.exists() or tc_path.mkdir()

        tcw = TestCaseWriter(tc_path, self.inputs, self.outputs)
        tcw.write()

        # Create verification case folder, to be left empty
        vc_path = target_folder / "verification_cases"
        vc_path.exists() or vc_path.mkdir()


# === READMEWriter Class ===
class READMEWriter():
    """
    To handle writing README.md
    """
    def __init__(self, path, title, link, version="4.0"):
        self.path = Path(path)
        self.title = title
        self.link = link
        self.version = version

    
    def write(self):
        """
        Writes to the README file in the given directory.
        """
        # Open path
        with self.path.open("w") as fw:
            # Title
            fw.write(f"# {self.title}")

            # Auto-generation statement
            fw.write(f"\n*This README.md is instantiated by HackerRank Coding Template Version {self.version}")

            # Link to problem
            fw.write(f"\n\nThis problem can be found [here]({self.link}).")        


# === TestFunctionWriter Class ===
class TestFunctionWriter():
    """
    Copies contents of test_functions.py and pastes them in the given destination.
    """
    def __init__(self, path):
        self.path = path


    def write(self):
        """
        Copies and writes.
        """
        contents = None 

        with open("test_functions.py", "r") as fr: 
            contents = fr.read() 

        with self.path.open("w") as fw:
            fw.write(contents)


# === FunctionWriter Class ===
class FunctionWriter(): 
    """
    To handle writing functions.py
    """
    def __init__(self, path, imports, function, main):
        self.path = path
        self.imports = imports
        self.function = function
        self.main = main

    
    def write(self):
        """
        Handles the function writing. This is intricately mixed with 'functions_base.py' and should be changed if there is a change in the aforementioned file.
        """
        base_main = None
        base_workspace = None

        with open("functions_base.py", "r") as fr:
            contents = fr.read().split("\n")

            base_main = contents[8:20]
            base_workspace = contents[21:]

        with self.path.open("w") as fw:
            # Write imports
            fw.write("# === Imports ===")
            
            for i in imports: 
                fw.write(f"\n{i}")

            # Write function
            fw.write("\n")
            fw.write("\n# === Function ===")
            fw.write(f"\n{self.function}")
            fw.write(f"\n    pass")

            # Write main() function header
            fw.write("\n\n")

            for line in base_main: 
                fw.write("\n")
                fw.write(line)

            # Write main function contents
            # Conditional check to ensure the remainder can be 'copy-pasted' in
            assert re.match("if __name__ == [\"']__main__[\"']", self.main[0])
            assert re.search("open\(.*\)", self.main[1])

            for line in self.main[3:]:
                fw.write("\n")
                fw.write(line)

            # Finish up with base workspace content
            fw.write("\n\n")

            for line in base_workspace:
                fw.write("\n")
                fw.write(line)


# === TestCaseWriter Class ===
class TestCaseWriter():
    """
    A class to write the test cases.
    """
    def __init__(self, path, inputs, outputs):
        # Check they are of equal length so they can be paired together
        assert len(inputs) == len(outputs) 

        self.path = path
        self.inputs = inputs
        self.outputs = outputs


    def write(self):
        # Write a test case for each input-output pair within the test file
        for x, (i, j) in enumerate(zip(self.inputs, self.outputs)):
            # Set x to string and buffer it with zeros until it is of length 2
            x = str(x) 
            x = "0" * (2 - len(x)) + x
            
            new_path = self.path / f"sample_case_{x}.txt"

            with new_path.open("w") as fw:
                fw.write(i)
                fw.write("\n---\n")
                fw.write(j)


# === BeautifulSoup wrapper function ===
def soup(s, parser="lxml"):
    """
    A wrapper function to handle BeautifulSoup defaults.
    """
    return BeautifulSoup(s, parser)


# === Script ===
from sys import argv
import json
from bs4 import BeautifulSoup
import re

if __name__ == "__main__":

    # === Set up console ===
    c = Console()

    # === Verify arguments ===
    c.start("Verifying script arguments")

    # The arguments passed are link, destination_folder, and an optional programming language. Thus, argv is of length 1 + 3 = 4
    try: 
        assert len(argv) in [2, 3, 4], "Incorrect number of arguments passed."
    except Exception as e:
        c.failure(e)

    # Load arguments
    # Link
    link = argv[1]

    # Destination
    dest = argv[2] if len(argv) == 3 and argv[2] != "-" else None

    # Language
    lang = argv[3] if len(argv) == 4 else None

    # Fill in dest and lang if None
    if dest is None or lang is None: 
        with open("configs.json", "r") as fr:
            configs = json.load(fr)

            if not dest: 
                dest = configs["destination"] 

            if not lang: 
                lang = configs["language"]

    # [TODO] Fix security issue of identifying python/hackerrank. Meanwhile, we overrwite dest with a parent folder, i.e. the folder is created in the same directory as this code.
    dest = str(Path().cwd())

    # Strip arguments
    link = link.strip()
    dest = dest.strip()
    lang = lang.strip()

    c.success()

    # === Set up script resources ===
    c.start("Setting up script resources")

    try:     
        # --- Parser ---
        p = Parser()

        # --- Driver ---
        d = Driver()

    except Exception as e:
        c.failure(e)

    c.success()

    # Encompass all following code in a try-except block to close d in case of a malfunction
    try: 

        # === Connect to website ===
        c.start("Connecting to HackerRank")

        try:
            d.goto(link)

            # Skip login prompt
            X_BUTTON_CLASS = "close-icon"

            d.wait(By.CLASS_NAME, X_BUTTON_CLASS).click()

        except Exception as e:
            c.failure(e)

        c.success()

        # === Verify programming language ===
        c.start(f"Verifying programming language: {lang}")

        try: 
            bs = soup(d.source())

            # Check that the correct language is selected
            LANG_BOX_CLASS = "css-1hwfws3"

            if bs.find("div", {"class": LANG_BOX_CLASS}) != lang:
                # The current language is not our language

                # Click on the language box
                d.d.find_element_by_class_name(LANG_BOX_CLASS).click()

                # Identify correct language
                LANG_LIST_ELEMENT_CLASS = "css-m62ux7"
                CORRECT_LANG_ID = None

                languages = soup(d.source()).find("div", {"class": LANG_LIST_ELEMENT_CLASS}).findChildren()

                for l in languages:
                    if l.getText() == lang:
                        CORRECT_LANG_ID = l.attrs["id"]

                assert CORRECT_LANG_ID is not None, "The desired programming language could not be found."

                # Set to correct language
                d.d.find_element_by_id(CORRECT_LANG_ID).click()

        except Exception as e: 
            c.failure(e)

        c.success()

        # === Identify meta information ===
        c.start("Identifying meta information")

        try: 
            bs = soup(d.source())

            # --- Title ---
            TITLE_CLASS = "text-headline"
            challenge_title = bs.find("div", {"class": TITLE_CLASS}).getText()

            # --- Sample inputs and outputs ---
            SAMPLE_INPUT_BODY_CLASS = "challenge_sample_input_body"
            sample_inputs = bs.findAll("div", {"class": SAMPLE_INPUT_BODY_CLASS})
            sample_inputs = [t.getText().strip() for t in sample_inputs]
            
            SAMPLE_OUTPUT_BODY_CLASS = "challenge_sample_output_body"
            sample_outputs = bs.findAll("div", {"class": SAMPLE_OUTPUT_BODY_CLASS})
            sample_outputs = [t.getText().strip() for t in sample_outputs]

            assert len(sample_inputs) == len(sample_outputs), "Error parsing sample inputs and sample outputs."

        except Exception as e:
            c.failure(e)

        c.success()

        # === Read online editor code ===
        c.start("Parsing online code")
        
        try: 
            # === Online code ===
            bs = soup(d.source())

            EDITOR_CLASS = "view-lines"
            EDITOR_LINE_CLASS = "view-line"
            
            editor_contents = bs.find("div", {"class": EDITOR_CLASS}).findAll("div", {"class": EDITOR_LINE_CLASS})
            editor_contents = [t.getText() for t in editor_contents]

            # Break into imports, def, and main
            imports = []
            function = None
            main = []

            for lx, line in enumerate(editor_contents): 
                # Parse
                s = p.parse(line)

                if re.match("import", s):
                    imports.append(s)

                elif re.match("def", s):
                    function = s

                elif re.match("if __name__", s):
                    main = editor_contents[lx:]
                    main = [p.parse(l) for l in main]

                    break

        except Exception as e:
            c.failure(e)

        c.success()

        # === Close driver ===
        c.start("Closing driver")

        try:
            d.close()

        except Exception as e: 
            c.failure(e) 

        c.success()

        # === Instantiate README ===
        c.start("Setting up workspace")
        
        try:
            fw = FolderWriter(dest, challenge_title, link, imports, function, main, sample_inputs, sample_outputs)
            fw.write()

        except Exception as e: 
            c.failure(e) 

        c.success()

        # === Resolve offline code ===

    
    except Exception as e:
        d.close()

        raise e