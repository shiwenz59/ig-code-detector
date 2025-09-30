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

To record the progress of each stages, we first create a database that serves as our 'state management' system for the pipeline. It has the structure below:
```json
{
  "pipeline_metadata": {
    "created_at": "2025-09-30T10:30:00Z",
    "last_updated": "2025-09-30T11:45:00Z",
    "version": "1.0",
    "total_accounts": 1,
    "total_contents": 0,
    "pipeline_status": "in_progress"
  },
  "accounts": [
    {
      "account_id": "teddavisdotorg",
      "account_url": "https://www.instagram.com/teddavisdotorg/",
      "status": "pending",
      "added_at": "2025-09-30T10:30:00Z",
      "last_processed": null,
      "metadata": {
        "total_posts": null,
        "posts_downloaded": 0,
        "posts_analyzed": 0,
        "posts_with_code": 0
      },
      "contents": [],
      "report": {
        "status": "not_started",
        "generated_at": null,
        "report_path": null
      },
      "errors": []
    }
  ]
}
```

Notice that we not yet have the content-specific statuses until we start discovering contents using our module. The data structure for contents looks like:
```json
{
  "contents": [
    {
      "content_id": "C12345ABC",
      "content_type": "video",
      "content_url": "https://www.instagram.com/p/C12345ABC/",
      "posted_at": "2025-09-15T14:22:00Z",
      "download": {
        "status": "completed",
        "started_at": "2025-09-30T10:35:00Z",
        "completed_at": "2025-09-30T10:35:30Z",
        "local_path": "./data/raw/teddavisdotorg/C12345ABC.mp4",
        "file_size_mb": 12.5,
        "error": null
      },
      "analysis": {
        "status": "completed",
        "started_at": "2025-09-30T10:36:00Z",
        "completed_at": "2025-09-30T10:37:15Z",
        "contains_code": true,
        "confidence": 0.87,
        "code_frame_ratio": 0.65,
        "frames_analyzed": 45,
        "code_frames_detected": 29,
        "detected_languages": ["processing", "javascript"],
        "error": null
      }
    }
  ]
}
```

## Download Module