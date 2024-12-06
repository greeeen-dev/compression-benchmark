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

import zstandard
import time
import os
from typing import Union

chunk_size = 4 * 1024 * 1024 # each chunk is 4MB
level = -7 # min compression

def compress(file: str) -> tuple[str, int, float]:
    """Compresses a file using Zstandard."""

    # open source file
    with open(file, 'rb') as f:
        data = f.read()

    # instantiate compressor
    compressor = zstandard.ZstdCompressor(threads=-1, level=level)

    # start timer
    t_start = time.time()

    # compress to LZMA
    with compressor.stream_writer(open('cache/compressed-n7.zst', 'wb')) as f:
        for i in range(0, len(data), chunk_size):
            f.write(data[i:i + chunk_size])

    # return filename and time taken
    return 'cache/compressed-n7.zst', os.path.getsize('cache/compressed-n7.zst'), time.time() - t_start

def decompress(file: str) -> tuple[Union[bytes, dict], float]:
    """Decompresses a file compressed using Zstandard."""

    # instantiate decompressor
    decompressor = zstandard.ZstdDecompressor()

    # prepare bytearray
    data = bytearray()

    # start timer
    t_start = time.time()

    # decompress from LZMA
    with decompressor.stream_reader(open(file, 'rb')) as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            data.extend(chunk)

    # return time taken
    return bytes(data), time.time() - t_start
