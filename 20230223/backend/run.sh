#!/bin/bash
cp ../dao.py .
cp ../common.py .
python3 api.py
rm dao.py
rm common.py
