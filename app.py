# simple_virtual_assistant.py

import datetime
import requests
import sqlite3
import logging

# --- Configuration ---
WEATHER_API_KEY = 'your_openweather_api_key_here'
LOG_FILE = 'assistant.log'
DB_FILE = 'history.db'

# --- Logging Setup ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- SQLite Setup (Optional) ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS operations (
                        id INTEGER PRIMARY KEY,
                        operation TEXT,
                        result TEXT,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

def log_to_db(operation, result):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('INSERT INTO operations (operation, result, timestamp) VALUES (?, ?, ?)',
                   (operation, str(result), timestamp))
    conn.commit()
    conn.close()

# --- Core Functions ---
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
    else:
        return "Failed to fetch weather. Check city name or API key."

def set_reminder(text, time):
    return f"Reminder set: '{text}' at {time}"

# --- Command Execution ---
def execute_command(command, inputs):
    if command == 'add':
        x, y = map(float, inputs)
        return add(x, y)
    elif command == 'subtract':
        x, y = map(float, inputs)
        return subtract(x, y)
    elif command == 'multiply':
        x, y = map(float, inputs)
        return multiply(x, y)
    elif command == 'divide':
        x, y = map(float, inputs)
        return divide(x, y)
    elif command == 'weather':
        return get_weather(inputs[0])
    elif command == 'reminder':
        return set_reminder(inputs[0], inputs[1])
    else:
        return "Unknown command. Type 'help' for options."

# --- Main Interface (Non-interactive wrapper for sandbox) ---
def main():
    init_db()
    print("Virtual Assistant Started (Non-Interactive Mode)")

    # Simulated command set (replace this with file input or CLI args as needed)
    commands = [
        ('add', ['5', '3']),
        ('subtract', ['10', '2']),
        ('multiply', ['4', '2']),
        ('divide', ['8', '2']),
        ('weather', ['London']),
        ('reminder', ['Meeting', '3:00 PM'])
    ]

    for cmd, args in commands:
        try:
            result = execute_command(cmd, args)
            print(f"Command: {cmd}, Result: {result}")
            if cmd in ['add', 'subtract', 'multiply', 'divide']:
                log_to_db(f"{cmd}({', '.join(args)})", result)
            if cmd == 'reminder':
                logging.info("Set reminder: %s at %s", args[0], args[1])
            if cmd not in ['help', 'exit']:
                logging.info(f"Executed {cmd} with args {args}, result: {result}")
        except Exception as e:
            print(f"Error executing {cmd}:", e)
            logging.error("Error performing %s: %s", cmd, e)

if __name__ == '__main__':
    main()
