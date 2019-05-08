#!/bin/sh

#sleep 60
echo "shell script start"
python3 script.py

echo "executed"

node tester.js

python3 sort.py

python3 scrape.py

python3 search.py

echo "The raw data with match percentage and URL is:-"
cat url_percent.json