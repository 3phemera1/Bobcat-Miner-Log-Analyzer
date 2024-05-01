#!/usr/bin/python3
import requests
import sys
from requests.auth import HTTPBasicAuth
import re
from datetime import datetime

def parse_line(line):
    beaconOutRegex = re.compile(r'poc beacon report')
    matchobject = beaconOutRegex.search(line)
    if matchobject:
        date_string = line.split()[0]
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        beaconIdRegex = re.compile(r'beacon_id="(.*?)"')
        matchobject = beaconIdRegex.search(line)
        print("Becaon at " + str(date_object) + "ID is: " + str(matchobject.group(1)))
#        print(line)

def main(argv):
    if len(argv) < 2:
        print("Usage: ./bobcatLogAnalyzer.py IP_ADDRESS")
        exit(1)
    IP = argv[1]
    url = 'http://' + IP + '/log/console.log'
    res = requests.get(url, auth=HTTPBasicAuth('bobcat', 'miner'))
    for line in res.iter_lines():
#        print(line.decode("ascii"))
        parse_line(line.decode("ascii"))



if __name__ == '__main__':
    main(sys.argv)
