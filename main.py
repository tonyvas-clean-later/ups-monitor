#!/usr/bin/python3

from os import path
from time import sleep
from datetime import datetime

# Custom monitor class
from monitor import Monitor

# Location of script
SCRIPT_DIR = path.normpath(path.dirname(__file__))
# Location of directory containing dump files
DUMP_DIR = f'{SCRIPT_DIR}/dump'
# Log file for monitor
LOG_FILE = f'{SCRIPT_DIR}/loggy.log'
# Frequency in seconds to poll status
POLL_INTERVAL_S = 5
# List of UPS to monitor
UPS_LIST = [
    'SMT1500RM2U-1'
]

# Log data to stdout and log file
def log(data):
    try:
        # Get date in format YYYY-MM-DD HH:MM:SS
        date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        line = f'{date} - {str(data)}'

        # Print and write line
        print(line)
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except Exception as e:
        print('Error: Failed to write to log: {e}')

# Create monitors
monitors = {}
for ups_name in UPS_LIST:
    monitors[ups_name] = Monitor(DUMP_DIR, ups_name)
    log(f'Created monitor for {ups_name}')

# Run monitors
while 1:
    for ups_name in monitors:
        result = monitors[ups_name].run()
        if not result['success']:
            # If failed to run, log it
            log(f'Error: failed to monitor {ups_name} - {result["error"]}')

    # Wait for next interval
    sleep(POLL_INTERVAL_S)