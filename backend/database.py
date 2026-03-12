import sqlite3
from sqlite3 import Connection, Cursor

con = Connection("database.db")

cur = con.cursor()

cur.execute("""CREATE TABLE admin (
            id INTEGER PRIMARY KEY,
            password TEXT NOT NULL)""")

cur.execute("""CREATE TABLE student (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            dob DATE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            degree TEXT NOT NULL,
            role TEXT DEFAULT 'student' NOT NULL
            )""")

cur.execute("""CREATE TABLE company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            HR_contact TEXT UNIQUE NOT NULL,
            website TEXT UNIQUE NOT NULL,
            approval_status TEXT NOT NULL DEFAULT 'pending',
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            industry TEXT)""")

cur.execute("""CREATE TABLE placement_drive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            job_description TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            deadline DATE NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE)""")

cur.execute("""CREATE TABLE application (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            drive_id INTEGER NOT NULL,
            date DATE NOT NULL,
            status TEXT NOT NULL DEFAULT 'applied',
            FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
            FOREIGN KEY (drive_id) REFERENCES placement_drive(id) ON DELETE CASCADE)""")

cur.execute("INSERT INTO admin (id, password) VALUES (1, 'admin123')")
con.commit()
con.close()