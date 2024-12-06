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

import lzma
import time
import os
from typing import Union

def compress(file: str) -> tuple[str, int, float]:
    """Compresses a file using LZMA."""

    # open source file
    with open(file, 'rb') as f:
        data = f.read()

    # start timer
    t_start = time.time()

    # compress to LZMA
    with lzma.open('cache/compressed.xz', 'wb') as f:
        f.write(data)

    # return filename and time taken
    return 'cache/compressed.xz', os.path.getsize('cache/compressed.xz'), time.time() - t_start

def decompress(file: str) -> tuple[Union[bytes, dict], float]:
    """Decompresses a file compressed using LZMA."""

    # start timer
    t_start = time.time()

    # decompress from LZMA
    with lzma.open(file, 'rb') as f:
        data = f.read()

    # return time taken
    return data, time.time() - t_start
