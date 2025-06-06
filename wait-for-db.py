#!/usr/bin/env python3
"""
Wait for database to be ready before starting the Flask application.
"""
import time
import psycopg2
import sys
import os

def wait_for_db():
    """Wait for database to be ready."""
    max_attempts = 30
    attempt = 1
    
    while attempt <= max_attempts:
        try:
            print(f"Attempt {attempt}/{max_attempts}: Trying to connect to database...")
            conn = psycopg2.connect(
                dbname='RSO',
                user='postgres',
                password='root',
                host='db',
                port='5432'
            )
            conn.close()
            print("Database is ready!")
            return True
        except psycopg2.OperationalError as e:
            print(f"Database not ready yet: {e}")
            if attempt == max_attempts:
                print("Max attempts reached. Exiting.")
                return False
            time.sleep(2)
            attempt += 1
    
    return False

if __name__ == "__main__":
    if wait_for_db():
        print("Starting Flask application...")
        # Import and run the Flask app
        os.execv(sys.executable, [sys.executable, "src/api.py"])
    else:
        print("Failed to connect to database. Exiting.")
        sys.exit(1)
