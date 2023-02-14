#!/bin/bash
cp ../dao.py .
python3 api.py
cp dao.py ..
rm dao.py
