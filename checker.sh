#!/bin/sh

#sleep 60
echo "shell script start"
python3 script.py
echo "executed"

node tester.js

python3 sort.py

python3 scrape.py
