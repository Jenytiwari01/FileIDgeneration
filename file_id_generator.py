import sqlite3
import os

class FileIDGenerator:
    def __init__(self, db_path="file_id.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_counter (
                rack INTEGER,
                row INTEGER,
                count INTEGER,
                PRIMARY KEY (rack, row)
            )
        ''')
        self.conn.commit()

    def get_max_rows(self, rack_number):
        if 1 <= rack_number <= 3:
            return 5
        elif rack_number == 4:
            return 3
        elif 5 <= rack_number <= 250:
            return 4
        elif 251 <= rack_number <= 360:
            return 5
        else:
            raise ValueError("Invalid rack number")

    def get_current_count(self, rack, row):
        cursor = self.conn.cursor()
        cursor.execute("SELECT count FROM file_counter WHERE rack=? AND row=?", (rack, row))
        result = cursor.fetchone()
        return result[0] if result else 0

    def update_count(self, rack, row, count):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO file_counter (rack, row, count)
            VALUES (?, ?, ?)
            ON CONFLICT(rack, row) DO UPDATE SET count=excluded.count
        ''', (rack, row, count))
        self.conn.commit()

    def generate_file_id(self, rack_number, row_number):
        if not (1 <= rack_number <= 360):
            raise ValueError("Rack number must be between 1 and 360")

        max_rows = self.get_max_rows(rack_number)
        if not (1 <= row_number <= max_rows):
            raise ValueError(f"Row number must be between 1 and {max_rows} for rack {rack_number}")

        current_count = self.get_current_count(rack_number, row_number)
        current_count = 0 if current_count >= 120 else current_count
        current_count += 1

        self.update_count(rack_number, row_number, current_count)

        rack_str = f"{rack_number:04d}"
        row_str = str(row_number)
        file_str = f"{current_count:03d}"
        return f"{rack_str}-{row_str}-{file_str}"

    def close(self):
        self.conn.close()

# CLI runner
def run_generator():
    generator = FileIDGenerator()

    print("File ID Generator")
    try:
        while True:
            try:
                rack = int(input("Enter Rack Number (1–360): "))
                row = int(input("Enter Row Number (check range based on rack): "))
                file_id = generator.generate_file_id(rack, row)
                print(f"Generated File ID: {file_id}")
            except ValueError as e:
                print(f"Error: {e}")

            again = input("Do you want to generate another File ID? (y/n): ").strip().lower()
            if again != 'y':
                break
    finally:
        generator.close()

if __name__ == "__main__":
    run_generator()
