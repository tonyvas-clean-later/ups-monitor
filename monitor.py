#!/usr/bin/python3

from subprocess import run, PIPE
from json import loads, dumps
from os import path
import time

class Monitor:
    def __init__(self, dump_dir, ups_name):
        self.dump_dir = dump_dir
        self.ups_name = ups_name

    def poll(self):
        result = { 'success': None, 'error': '', 'data': '' }

        proc = run(['upsc', self.ups_name], stdout=PIPE, stderr=PIPE)
        result['success'] = proc.returncode == 0
        result['error'] = proc.stdout.decode('utf-8')
        result['data'] = proc.stderr.decode('utf-8')

        return result

    def format(self, data):
        result = { 'success': None, 'error': '', 'data': '' }

        result['data'] = data

        return result

    def write(self, data):
        result = { 'success': None, 'error': '', 'data': '' }

        return result

    def run(self):
        result = { 'success': None, 'error': '', 'data': '' }

        poll_result = self.poll()
        if not poll_result['success']:
            result['success'] = False
            result['error'] = 'Failed to poll: ' + poll_result['error']
            return result

        format_result = self.format(poll_result['data'])
        if not format_result['success']:
            result['success'] = False
            result['error'] = 'Failed to format: ' + format_result['error']
            return result

        write_result = self.write(format_result['data'])
        if not write_result['success']:
            result['success'] = False
            result['error'] = 'Failed to write: ' + write_result['error']
            return result
