# 📦 Seed Script for MySQL Database

This script (`seed.py`) sets up the MySQL database and populates it with data from a CSV file.

## ✅ What it does

1. Connects to MySQL server.
2. Creates the database `ALX_prodev` if it doesn't exist.
3. Connects to the `ALX_prodev` database.
4. Creates the `user_data` table if it doesn't exist.
5. Reads sample data from `user_data.csv`.
6. Inserts data into the table (skips duplicates based on email).

## 🗂️ Folder Structure

alx-backend-python/
│
├── seed.py
├── user_data.csv
└── README.md

## 🛠️ Usage

Run the script to seed the database:

```bash
python seed.py
```

Make sure your **MySQL server is running** and you have the right credentials.

## 📋 Table Structure: `user_data`

| Field    | Type            | Constraints          |
|----------|-----------------|---------------------|
| user_id  | CHAR(36)        | Primary Key, UUID   |
| name     | VARCHAR(255)    | NOT NULL            |
| email    | VARCHAR(255)    | NOT NULL            |
| age      | DECIMAL(10,0)   | NOT NULL            |

## 📄 CSV Example (`user_data.csv`)

name,email,age
John Doe,<john.doe@example.com>,28
Jane Smith,<jane.smith@example.com>,34

## 🐍 Requirements

- Python 3.x
- `mysql-connector-python`

Install dependencies:

```bash
pip install mysql-connector-python
```

## 📝 Notes

- Existing records are **not duplicated** (checked by email).
- UUIDs are generated for each user.
- Simple error handling is included.
