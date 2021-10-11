#!/usr/bin/python3

import json
import os
from subprocess import Popen, PIPE
import sys

base_path = f"{ os.getcwd() }/__tests__/"


def print_test_status(is_success, product, test_type):
    print()
    print("=" * 15, "Test result", "=" * 15)
    print("PASS" if is_success else "FAIL", f"— {product} ({test_type})")
    print("=" * 43)


def xpub_scan(data, filepath):
    xpub = data['xpub']
    coin = data['coin_ticker']

    cmd = f"node lib/scan.js {xpub} --currency {coin} --operations {filepath} --diff --custom-provider --quiet"

    with Popen(cmd.split(), stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')

    return p.returncode


def run_positive_test(data):
    filepath = f"{base_path}/datasets/positive_tests/{data['filename']}"

    return_code = xpub_scan(data, filepath)

    # positive test passes if the command does not fail
    is_success = return_code == 0

    print_test_status(is_success, data['product'], "positive test")


def run_negative_test(data):
    filepath = f"{base_path}/datasets/negative_tests/{data['filename']}"

    return_code = xpub_scan(data, filepath)

    # negative test passes if the command fails
    is_success = return_code != 0

    print_test_status(is_success, data['product'], "negative test")


if __name__ == "__main__":
    with open(f"{base_path}/datasets.json", 'r') as f:
        dataset = json.load(f)

    for data in dataset:
        test_types = data['test_types']

        for test_type in test_types:
            is_success = run_positive_test(
                data) if test_type == "positive" else run_negative_test(data)

            if not is_success:
                sys.exit(1)
