# === FolderWriter Class ===
from pathlib import Path
import re

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
    def __init__(self, path, title, link, version="5.0"):
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
            
            for i in self.imports: 
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
            # assert re.match("if __name__ == [\"']__main__[\"']", self.main[0])
            # assert re.search("open\(.*\)", self.main[1])

            for line in self.main[1:]:
                # If there is an open() function, do not write
                if re.search("open(.*)", line):
                    continue

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