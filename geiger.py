#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Counts Per Minute and uSv/h initialization
cpm = 0
counts = 0
usvh_ratio = 0.00584666666667   # Conversion factor from CPM to uSv/h  previously used 0.00812037037037  also 0.00332 
usvh = 0  # Initialize microsieverts per hour

# Time tracking
current_time = int(time.time())
avg_over = 5  # seconds - pick one of 5, 10, 15, 30, 60
start_time = current_time  # Time the application started

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/data")
def get_data():
    # Returns the current CPM and uSv/h as JSON
    return jsonify({
        'cpm': cpm,
        'usvh': usvh
    })

def log_to_terminal():
    """
    Logs the CPM and uSv/h to the terminal, similar to how it would be done in the Arduino code.
    """
    minutes_running = (int(time.time()) - start_time) / 60  # Calculate minutes since the start
    if minutes_running < 1:
        minutes_running = 1  # Ensure at least 1 minute is used for calculations
    
    #print(f"Total clicks since start: {counts}")
    print(f"Rolling CPM: {cpm}")
    print(f"uSv/h: {usvh:.4f}")
    print("---------------------\n")
    #print(f"Minutes since start: {minutes_running:.2f}\n")

def on_event(channel):
    global counts, cpm, usvh, current_time
    counts += 1  # Increment the count every time an event occurs (a pulse detected)

    # Update CPM and uSv/h at regular intervals (every 'avg_over' seconds)
    if int(time.time()) >= current_time + avg_over:
        # Calculate counts per minute based on events in the last `avg_over` seconds
        cpm = counts * (60 // avg_over)

        # Calculate uSv/h based on the counts using the provided ratio
        usvh = cpm * usvh_ratio  # uSv/h is proportional to CPM
        
        # Log the values to the terminal (console)
        log_to_terminal()
        
        counts = 0  # Reset counts for the next period
        current_time = int(time.time())  # Reset current time

# Set up GPIO pin for input (use the appropriate pin for your hardware)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.add_event_detect(7, GPIO.FALLING, callback=on_event)

if __name__ == '__main__':
    # Run the Flask app
    app.run(ssl_context=('cert.pem', 'key.pem'), host="0.0.0.0", port=80, debug=False)
