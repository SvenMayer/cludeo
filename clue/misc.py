# -*- coding: utf-8 -*-
import random
import time
import sys

if sys.version_info[0] > 2:
    random.seed(time.perf_counter())
else:
    random.seed(time.clock())


def random_integer(max_int):
    res = max_int + 1
    while res > max_int:
        res = int(random.random() * (max_int + 1))
    return res