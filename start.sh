#!/bin/bash

cd $(dirname "${BASH_SOURCE[0]}")

if [ ! -d env ]; then
  virtualenv env
  . env/bin/activate
  env/bin/pip3 install -r deps.txt
else
  . env/bin/activate
fi

python3 main.py

deactivate

exit 0
