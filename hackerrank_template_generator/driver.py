# === Webdriver Class ===
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
from selenium.webdriver.remote.remote_connection import LOGGER

import os

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
                    if cd != cd.parent: 
                        cd = cd.parent 

                    else:
                        raise Exception("geckodriver.exe not found.")

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
        self.d = webdriver.Firefox(executable_path=gecko, options=o, service_log_path=os.devnull)

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


def by(s): 
    """
    Returns By constants for the driver.
    """
    s = s.lower()

    if s == "id": 
        return By.ID

    elif s == "class_name":
        return By.CLASS_NAME