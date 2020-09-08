# === Imports ===
from pathlib import Path
import json 

from console import Console
from char_parser import Parser
from driver import Driver, by
from writers import FolderWriter
from soup import soup

from sys import argv
import requests
import io 
from zipfile import ZipFile

import re

# === Setup ===
# Load configs
conf_file = Path().cwd() / "configs.json"

with conf_file.open("r") as fr: 
    configs = json.load(fr)

website_link = configs["website_link"]

# === Script ===
if __name__ == "__main__":

    # === Set up console ===
    c = Console()

    # === Obtain and verify script arguments ===
    c.start("Verifying script arguments")

    # Only the link needs to be passed.
    try: 
        assert len(argv) == 2, "Incorrect number of arguments passed."
    except Exception as e:
        c.failure(e)

    # Load link
    link = argv[1].strip()
    
    c.success()

    # === Set up Parser() resource ===
    c.start("Setting up string parser resources")
    
    try: 
        p = Parser()

    except Exception as e: 
        c.failure(e) 

    c.success()

    # === Set up Driver() resource ===
    c.start("setting up driver resources")

    try: 
        d = Driver()

    except Exception as e:
        c.failure(e) 

    c.success()

    # Encompass the code in a try-except to force driver shutdown
    try: 
        
        # === Connect to website ===
        c.start(f"Connecting to {configs['website_name']}")

        try: 
            d.goto(link)

            # Skip login prompt
            X_BUTTON_CLASS = "close-icon"

            d.wait(by("class_name"), X_BUTTON_CLASS).click()

        except Exception as e:
            c.failure(e)

        c.success()

        # === Verify programming language ===
        lang = configs['language']

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

        # === Identify challenge information ===
        # --- Title ---
        c.start("Identifying challenge information: Title")

        try: 

            TITLE_CLASS = "text-headline"
            challenge_title = bs.find("div", {"class": TITLE_CLASS}).getText()    
        
        except Exception as e: 
            c.failure(e)

        c.success()

        # --- Difficulty ---
        c.start("Identifying challenge information: Difficulty")

        try: 
            DIFF_BLOCK_CLASS = [
                "sidebar-problem-difficulty",
                "challenge-sidebar-help"
            ]
            DIFF_BLOCK_LEVEL_CLASS = "pull-right"

            diff_block = bs.find("div", {"class": DIFF_BLOCK_CLASS})

            diff_block = list(filter(lambda x: "Difficulty" in x.getText(), diff_block))[0].find("p", {"class": DIFF_BLOCK_LEVEL_CLASS})

            difficulty = diff_block.getText()

        except Exception as e: 
            c.failure(e)

        c.success()

        # --- Inputs and outputs ---
        c.start("Identifying challenge information: Sample inputs and outputs")

        try: 
            bs = soup(d.source())        

            # --- Sample inputs and outputs ---
            SAMPLES_DOWNLOAD_ID = "test-cases-link"
            samples_link = bs.find("a", id=SAMPLES_DOWNLOAD_ID)

            assert samples_link.attrs["href"]

            # Download
            samples_link = f"{website_link}{samples_link.attrs['href']}"

            headers = {'User-Agent': 'Mozilla'}
            samples = requests.get(samples_link, stream=True, headers=headers)

            # Obtain zip file
            zipfile = ZipFile(io.BytesIO(samples.content))

            zip_names = zipfile.namelist()

            zipfiles = []

            for file_name in zip_names: 
                
                name = Path(file_name).name
                content = zipfile.open(file_name).read().decode('utf-8').strip()

                # Only add if there's content

                if content: 

                    zipfiles.append({
                        "name": name,
                        "content": content
                    })

            # The files come in input00.txt and output00.txt format
            # Thus, we want to assert that all files come in this format and match them to each other
            test_cases = {}

            for f in zipfiles: 

                case_re = re.search("(output|input)(\d+).txt", f["name"])

                assert case_re, "Unsupported test case format."

                case_type = case_re.group(1)
                case_num = case_re.group(2)

                if case_num not in test_cases.keys():
                    test_cases[case_num] = {}

                test_cases[case_num][case_type] = f["content"]

            # Collected samples
            sample_inputs = []
            sample_outputs = []

            for tc in test_cases.values():

                assert "input" in tc.keys() and "output" in tc.keys()
                
                sample_inputs.append(tc["input"])
                sample_outputs.append(tc["output"])
    
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
        
        # Set destination into the difficulty level
        dest = Path().cwd().parent.parent / difficulty

        try:
            fw = FolderWriter(dest, challenge_title, link, imports, function, main, sample_inputs, sample_outputs)
            fw.write()

        except Exception as e: 
            c.failure(e) 

        c.success()

    except Exception as e:
        # d.close()

        raise e