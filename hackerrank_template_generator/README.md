# HackerRank Template Generator v5.0

## Changes from v4.0
1. [ ] Removal of verification cases
 The verifications folder has been removed, to emphasise the need for a proof-of-concept code using the cases in `test_cases`.

1. [x] Sample cases
 Sample cases will be directly downloaded from HackerRank, with the download stored in RAM to avoid writing to memory. This overcomes certain problems with scraping the page for sample test cases.

1. [x] Difficulty level
 Challenges will be automatically added to their relevant difficulty folders. 

## Resources
* [Downloading file using `requests` directly to memory](https://stackoverflow.com/questions/22340265/python-download-file-using-requests-directly-to-memory)
* [Downloading and unzipping a zip file without writing to disk](https://stackoverflow.com/questions/5710867/downloading-and-unzipping-a-zip-file-without-writing-to-disk)

## Instructions
Simply run `python download.py "link"`, replacing 'link' with the link to the HackerRank page containing the challenge. 
This has not been proven to work on all HackerRank challenges. 