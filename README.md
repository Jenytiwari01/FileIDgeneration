File ID Generator
A Python application for generating unique File IDs in a file management system. Uses SQLite for persistence and follows a specific rack-row-file numbering scheme.
How it works
The system generates File IDs in the following format: 
RackNumber-RowNumber-FileNumber
For example: 0001-2-045
ID Components
•	Rack Number: 4-digit number with leading zeros (0001-0360)
•	Row Number: Depends on which rack you're using (1-5 rows)
•	File Number: 3-digit number that counts up from 001 to 120, then starts over
Rack Setup
We have 360 racks total, but they don't all have the same number of rows:
Racks	Rows	Notes
1-3	5	First few racks
4	3	Special case - fewer rows
5-250	4	Most of our racks
251-360	5	Extended section
What you need
•	Python 3.6 or newer
•	That's it - SQLite comes with Python
Getting started
Just run:
python task.py
The program will walk you through entering rack and row numbers, then give you a File ID.
Example run
File ID Generator with SQLite Persistence
Enter Rack Number (1–360): 15
Enter Row Number (check range based on rack): 2
Generated File ID: 0015-2-001
Do you want to generate another File ID? (y/n): y
Enter Rack Number (1–360): 15
Enter Row Number (check range based on rack): 2
Generated File ID: 0015-2-002
Do you want to generate another File ID? (y/n): n
Some examples
•	First file in rack 1, row 2: 0001-2-001
•	45th file in rack 4, row 3: 0004-3-045
•	120th file in rack 150, row 1: 0150-1-120
•	Next file after hitting 120: 0300-5-001 (counter resets)
Files
•	task.py - the main program
•	file_id.db - SQLite database (gets created automatically)
How the database works
Simple table that keeps track of file counts for each rack/row combination:
CREATE TABLE file_counter (
    rack INTEGER,
    row INTEGER,
    count INTEGER,
    PRIMARY KEY (rack, row)
)
Code structure
FileIDGenerator class
Main class that handles the ID generation logic.
Key methods:
•	__init__(db_path="file_id.db") - Sets up the database connection
•	get_max_rows(rack_number) - Tells you how many rows a rack has
•	generate_file_id(rack_number, row_number) - Makes a new File ID
•	close() - Cleans up the database connection
Internal stuff:
•	_create_table() - Sets up the database table if needed
•	get_current_count(rack, row) - Gets the current file count
•	update_count(rack, row, count) - Updates the count in the database
Database persistence
The app remembers where you left off between runs by storing counts in SQLite. Each rack/row combo gets its own counter that picks up where it left off.
Error handling
The program handles common mistakes:
•	Rack numbers outside 1-360 range
•	Row numbers that don't exist for a given rack
•	Database connection problems
•	Non-numeric input
•	File numbers automatically wrap from 120 back to 001
Notes
•	Each rack/row combination has its own independent file counter
•	Counters persist between program runs
•	File numbers reset to 001 after reaching 120
•	Database connections are properly cleaned up when done
