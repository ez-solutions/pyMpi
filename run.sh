#!/bin/sh
# SIZE=""
# python serial_pi()
# python -c "import mpi4py"
# MSG=$?
# if [ "$MSG" != "0" ]; then
#     echo "mpi4py is installed"
mpiexec -np 4 python pympi.py
# else
#     echo "mpi4py no found"
python serial_pi.py
# fi