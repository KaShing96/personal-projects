# === Soup Wrapper ===
from bs4 import BeautifulSoup

def soup(s, parser="lxml"):
    """
    A wrapper function to handle BeautifulSoup defaults.
    """
    return BeautifulSoup(s, parser)