avatarUp.py
Additional improvements to consider:

Add error handling for specific API errors (e.g., rate limiting, authentication issues).
Implement retries for transient errors.
Add a timeout for API calls to prevent the script from hanging indefinitely.
Validate the structure of the extracted JSON against a schema to ensure it contains the expected fields.
Implement a more sophisticated logging system that can handle different log levels and rotate log files.
Add unit tests for the new extract_json_from_response function and other critical parts of the
