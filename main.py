"""
MIT License

Copyright (c) 2024-present Green (@greeeen-dev)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import importlib
import sys
import string
import random
import os

# load config
with open('config.json', 'r') as f:
    config = json.load(f)

# check if there's no tests
if len(config['formats']) == 0:
    print('Nothing to do')
    sys.exit(0)

# purge cache
for file in os.listdir('cache'):
    if file == '.gitignore' or file == 'README.md':
        continue
    try:
        os.remove(f'cache/{file}')
    except:
        pass

# generate random data
random_data = {}
for _ in range(config['size']):
    key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
    value = {}

    for _ in range(config['nested_size']):
        nested_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
        nested_value = ''.join(random.choices(string.ascii_lowercase + string.digits, k=128))
        value.update({nested_key: nested_value})

    random_data.update({key: value})

# save random data to uncompressed json
with open('cache/data.json', 'w') as f:
    # noinspection PyTypeChecker
    json.dump(random_data, f, indent=4)

def main():
    # run compression tests
    for compression_format in config['formats']:
        # import test module
        try:
            compression_module = importlib.import_module(f'formats.{compression_format[1]}')
        except ImportError:
            print(f'Failed to import {compression_format[0]}\'s test module, skipping test...\n')
            continue

        # run compression and decompression tests
        filename, filesize, c_duration = compression_module.compress('cache/data.json')
        returned_data, d_duration = compression_module.decompress(filename)

        # convert data to dict if it's in bytes
        if type(returned_data) is bytes:
            decoded = json.loads(returned_data.decode('utf-8'))
        else:
            decoded = returned_data

        # check if data is correct, otherwise raise warning
        if decoded != random_data:
            print(f'{compression_format[0]} did not decompress data correctly.\n')

        # output result
        print(f'{compression_format[0]}: {round(c_duration, 2)}s compress to {round(filesize/1024/1024,2)}MB, {round(c_duration, 2)}s decompress\n')


if __name__ == '__main__':
    main()
    print('Tests completed, exiting...')
