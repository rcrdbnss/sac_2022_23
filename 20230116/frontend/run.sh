#!/bin/bash
cp ../dao.py .
cp ../common.py .
python3.9 main.py
rm dao.py
rm common.py
