#!/bin/python

import imp
import sys

try:
    imp.find_module('mpi4py')
    found = True
    import mpi4py
except ImportError:
    sys.exit("mpi Module not found.")
# python -c "import mpi" && echo $?