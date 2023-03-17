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
    monitors[ups_name] = Monitor(DUMP_DIR, POLL_INTERVAL_S, ups_name)