import gc
import os
import sys
from machine import freq

from .base import BaseCommand


class SysInfo(BaseCommand):
    name = 'sysinfo'
    description = 'Show system information.'

    def __call__(self, params: list) -> None:
        gc.collect()

        mem_alloc = gc.mem_alloc()
        mem_free  = gc.mem_free()
        mem_total = mem_alloc + mem_free

        fs = os.statvfs('/')
        fs_block_size = fs[0]
        fs_total      = fs[2] * fs_block_size
        fs_free       = fs[3] * fs_block_size

        print(f"{'Platform':<16}: {sys.platform}")
        print(f"{'Machine':<16}: {sys.implementation._machine}")
        print(f"{'MicroPython':<16}: {sys.version}")
        print(f"{'CPU freq':<16}: {freq() // 1_000_000} MHz")
        print(f"{'RAM total':<16}: {mem_total // 1024} kB")
        print(f"{'RAM used':<16}: {mem_alloc // 1024} kB")
        print(f"{'RAM free':<16}: {mem_free // 1024} kB")
        print(f"{'Flash total':<16}: {fs_total // 1024} kB")
        print(f"{'Flash free':<16}: {fs_free // 1024} kB")
