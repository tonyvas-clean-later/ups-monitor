#!/usr/bin/python3

from subprocess import run, PIPE
from json import loads, dumps
from os import path
from datetime import datetime

class Monitor:
    # Initialise instance
    def __init__(self, dump_dir, ups_name):
        self.dump_dir = dump_dir
        self.ups_name = ups_name

    # Generate a result object
    def generate_result(self, success, error, data):
        return { 'success': success, 'error': str(error), 'data': str(data) }

    # Generate a successful result object
    def generate_result_success(self, data):
        return self.generate_result(True, None, data)

    # Generate an error result object
    def generate_result_error(self, error):
        return self.generate_result(False, error, None)

    # Poll upsc for UPS status
    def poll(self):
        # Run the subprocess
        proc = run(['upsc', self.ups_name], stdout=PIPE, stderr=PIPE)
        
        # Check exit code of process and generate result
        if proc.returncode != 0:
            return self.generate_result_error(proc.stderr.decode('utf-8'))
        else:
            return self.generate_result_success(proc.stdout.decode('utf-8'))

    # Format result data from polling into a nicer output
    def format(self, data):
        try:
            json_obj = {}
            # Loop over each line
            for line in data.strip().split('\n'):
                # Split line into key/value pair and add to obj
                [key, value] = line.strip().split(': ')
                json_obj[key] = value

            # Return json string data result
            return self.generate_result_success(dumps(json_obj))
        except Exception as e:
            return self.generate_result_error(e)

    # Write UPS status to dump file
    def write(self, data):
        try:
            # Get date formatted as YYYY-MM-DD
            date = datetime.today().strftime('%Y-%m-%d')
            # Get time formatted as HH:MM:SS
            time = datetime.today().strftime('%H:%M:%S')
            # Path to write to
            dump_file = path.join(self.dump_dir, f'{self.ups_name}_{date}')
            
            # Open and append time and data to dump file
            with open(dump_file, 'a') as f:
                f.write(f'{time} - {data}\n')

            return self.generate_result_success('Successfully written!')
        except Exception as e:
            return self.generate_result_error(e)

    # Run iteration of monitor
    def run(self):
        # Poll status
        poll_result = self.poll()
        if not poll_result['success']:
            # Generate error result if failed to poll
            return self.generate_result_error('Failed to poll: ' + poll_result['error'])

        # Format polled result data
        format_result = self.format(poll_result['data'])
        if not format_result['success']:
            # Generate error result if failed to format
            return self.generate_result_error('Failed to format: ' + format_result['error'])

        # Write formatted status to dump file
        write_result = self.write(format_result['data'])
        if not write_result['success']:
            # Generate error result if failed to write
            return self.generate_result_error('Failed to write: ' + write_result['error'])

        # End with a success result
        return self.generate_result_success('Success!')