# ig-code-detector

## Task

We aim to design a pipeline that automatically query instagram accounts and their contents and detect if codes are included. The major stages of the program are:
1. Input: The account, or list of accounts, to query
2. Media download (iterative)
3. Code detection (iterative)
4. Output: Report

Some additional requirements we have are:
* The UI should be intuitive and allows for efficient processing
* The process should incorporate parallel computing to be efficient
* The program should be interpretable so users can see stages of the pipeline
* The resulting report should be structural and understandable

## High-Level Architecture
![high-level architecture](./report-materials/architecture.png)
To summarize, the elements we have in the pipeline are:
* Module to download all contents under an account
* Module to detect codes in one piece of content
* Temporary database to store downloaded contents
* Database to hold output reports

## Input and UI
![ui](./report-materials/ui.001.png)
Users can input a list of links to the account they wish to be examined. Once they started the program, they will be able to track the process of the program, including how many accounts and contents have been detected as well as the status of generated reports.