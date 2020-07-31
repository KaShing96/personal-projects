# HackerRank Coding Template Version 4.0
 - [X] We attempt to improve the modularity of the code from 3.0. 
 - [X] Furthermore, instead of editing existing files, we will generate a new file in the desired location. 

## Problems
Currently, for security reasons, we do not add the absolute path of the destination to the configs.json or to the script. Thus, we are unable to locate python/hackerrank to create the new folder as we do not want to assume folder creation in a folder arbitrarily 2 levels higher. Instead, for consistency, the new folder will be created in this subdirectory.

The script also fails in extracting sample cases for certain HackerRank challenges, such as the one [here](https://www.hackerrank.com/challenges/anagram/problem?utm_campaign=challenge-recommendation&utm_medium=email&utm_source=24-hour-campaign).

## Instructions
Simply run python setup.py "link", replacing 'link' with the link to the HackerRank page containing the challenge. This has not been proven to work on all HackerRank challenges. 