# File ID Generator 

A Python application for generating unique File IDs in a file management system. Uses SQLite for persistence and follows a specific rack-row-file numbering scheme.

## Table of Contents

- [Overview](#overview)
- [File ID Format](#file-id-format)
- [Rack Configuration](#rack-configuration)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Database Structure](#database-structure)
- [Code Structure](#code-structure)
- [Error Handling](#error-handling)
- [Features](#features)

## Overview

The File ID Generator creates unique identifiers for files in a warehouse-style management system. Each file is assigned a unique ID based on its physical location (rack and row) and maintains sequential numbering within each location.

## File ID Format

File IDs follow the format: `RackNumber-RowNumber-FileNumber`

**Example:** `0001-2-045`

### ID Components

| Component | Description | Format | Range |
|-----------|-------------|---------|--------|
| **Rack Number** | 4-digit number with leading zeros | `0001` | 0001-0360 |
| **Row Number** | Depends on rack configuration | `2` | 1-5 (varies by rack) |
| **File Number** | 3-digit sequential counter | `045` | 001-120 (then resets) |

## Rack Configuration

Our warehouse contains **360 racks** with varying row configurations:

| Rack Range | Rows | Notes |
|------------|------|-------|
| `1-3` | 5 | First few racks |
| `4` | 3 | Special case - fewer rows |
| `5-250` | 4 | Most of our racks |
| `251-360` | 5 | Extended section |

## Requirements

- **Python 3.6** or newer
- **SQLite** (included with Python)

That's it! No additional dependencies required.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/file-id-generator.git
   cd file-id-generator
   ```

2. Run the application:
   ```bash
   python task.py
   ```

## Usage

### Basic Example

```bash
$ python task.py

File ID Generator with SQLite Persistence
Enter Rack Number (1–360): 15
Enter Row Number (check range based on rack): 2
Generated File ID: 0015-2-001

Do you want to generate another File ID? (y/n): y
Enter Rack Number (1–360): 15
Enter Row Number (check range based on rack): 2
Generated File ID: 0015-2-002

Do you want to generate another File ID? (y/n): n
```

### Example File IDs

- First file in rack 1, row 2: `0001-2-001`
- 45th file in rack 4, row 3: `0004-3-045`
- 120th file in rack 150, row 1: `0150-1-120`
- Next file after hitting 120: `0150-1-001` (counter resets)

## Database Structure

The application uses SQLite to maintain persistence between runs.

### Files Created
- `task.py` - Main application
- `file_id.db` - SQLite database (auto-created)

### Database Schema

```sql
CREATE TABLE file_counter (
    rack INTEGER,
    row INTEGER,
    count INTEGER,
    PRIMARY KEY (rack, row)
);
```

Each rack/row combination maintains its own independent file counter.

## Code Structure

### `FileIDGenerator` Class

The main class handling ID generation logic:

#### Key Methods

| Method | Description |
|--------|-------------|
| `__init__(db_path="file_id.db")` | Sets up database connection |
| `get_max_rows(rack_number)` | Returns max rows for a given rack |
| `generate_file_id(rack_number, row_number)` | Creates a new File ID |
| `close()` | Cleans up database connection |

#### Internal Methods

- `_create_table()` - Sets up database table if needed
- `get_current_count(rack, row)` - Gets current file count
- `update_count(rack, row, count)` - Updates count in database

## Error Handling

The application handles common input errors:

- Rack numbers outside 1-360 range
- Invalid row numbers for specific racks
- Database connection problems
- Non-numeric input validation
- Automatic file number wrapping (120 → 001)

## Features

- **Persistent Counters**: Each rack/row combination maintains independent counters
- **Automatic Reset**: File numbers reset to 001 after reaching 120
- **Database Persistence**: Counters persist between program runs
- **Error Validation**: Comprehensive input validation
- **Clean Architecture**: Modular, object-oriented design
- **Zero Dependencies**: Uses only Python standard library

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/Jenytiwari01/FileIDgeneration/issues) on GitHub.

---

<div align="center">
  <strong>Made with ❤️ for efficient file management</strong>
</div>
