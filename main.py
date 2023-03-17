#!/usr/bin/python3

from os import path
from monitor import Monitor

SCRIPT_DIR = path.normpath(path.dirname(__file__))
DUMP_DIR = f'{SCRIPT_DIR}/dump'
POLL_INTERVAL_S = 1
UPS_LIST = [
    'SMT1500RM2U-1'
]

monitors = {}
for ups_name in UPS_LIST:
    monitors[ups_name] = Monitor(DUMP_DIR, ups_name)

for ups_name in monitors:
    result = monitors[ups_name].run()
    if result['success']:
        print(ups_name, result['data'])
    else:
        print(ups_name, result['error'])