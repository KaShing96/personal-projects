# Personal Projects
A repository to keep track of my personal projects. All the projects here have reached some form of conclusion, whether they are completed or discontinued. 

# HackerRank Template Generator v4.0
The HackerRank Template Generator sets up an offline programming environment purposed to debug HackerRank challenges. From a given link, it extracts the challenge's title, sample inputs and outputs, and the code under `if __name__ == '__main__':` (for Python 3) to parse through the challenge's inputs and outputs. The debugging is developed with `pytest`.

The environment is generated with the following command:
```
python setup.py "<hackerrank link>"
```
It can then be debugged with the `pytest` module, such as calling the following command in the environment's directory:
```
py.test
```
## Problems
1. **Integration with verification cases**<br>v4.0 is built with the intention of debugging both test and verification cases, though verification cases should not be debugged. They should serve as confirmations of a solution's viability. 
2. **Target directory**<br>The debugging environment is currently created in the same directory as the generator script. While adding an additional argument for the target destination is possible, it necessitates copy-pasting two paths (the HackerRank link and the path to the destination), which makes it less streamlined to use.
3. **Sample cases**<br>Currently, not all sample cases can be scraped by the script. Certain older problems do not share the same CSS classes as newer problems; the script is only tuned to newer problems.

## To-Do
 - [ ] Remove the creation of the verification cases folder to highlight the importance of using test cases as a proof-of-concept of the solution.
 - [ ] Extract further meta-data, such as the difficulty level of the HackerRank solution, to be directly added into the README.
 - [ ] Increase the modularity of the code to add support for other languages, apart from Python 3. 