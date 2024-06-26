#!/usr/bin/python3
import requests
import sys
from requests.auth import HTTPBasicAuth
import re
from datetime import datetime
import os.path

def parse_line(line):
    beaconOutRegex = re.compile(r'poc beacon report')
    matchobject = beaconOutRegex.search(line)
    if matchobject:
        date_string = line.split()[0]
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        beaconIdRegex = re.compile(r'beacon_id="(.*?)"')
        matchobject = beaconIdRegex.search(line)
        print("Becaon at " + str(date_object) + "   ID is: " + str(matchobject.group(1)))
    beaconRxRegex = re.compile(r'received potential beacon')
    matchobject = beaconRxRegex.search(line)
    if matchobject:
        date_string = line.split()[0]
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        pattern_dlm = r'downlink_mac=(.*?)'
        pattern_snr = r'snr: (-?\d+)'
        pattern_rssi = r'rssi: (-?\d+)'
        pattern_len = r'len: (\d+)'
        match_dlm = re.search(pattern_dlm, line)
        match_snr = re.search(pattern_snr, line)
        match_rssi = re.search(pattern_rssi, line)
        match_len = re.search(pattern_len, line)
        mac = match_dlm.group(1) if match_dlm else None
        snr = match_snr.group(1) if match_snr else None
        rssi = match_rssi.group(1) if match_rssi else None
        length = match_len.group(1) if match_len else None
        print("Received Possible Beacon at " + str(date_object) + ": MAC: " + str(mac) + " SNR: " + str(snr) + " rssi: " + str(rssi) + " packet_len: " + str(length))
    nextBeaconTimeRegex = re.compile(r'next beacon time')
    matchobject = nextBeaconTimeRegex.search(line)
    if matchobject:
        date_string = line.split()[0]
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        pattern_bt = r'beacon_time=(\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}\.\d+) (\S+)'
        match_bt = re.search(pattern_bt, line)
        nextbt_str = match_bt.group(1) if match_bt else None
        nextbt_offset_str = match_bt.group(2) if match_bt else None
        dt_with_offset_tz = str(nextbt_str) + " " + str(nextbt_offset_str)
        print("At " + str(date_object) + ": Next Beacon at: " + str(dt_with_offset_tz))



def main(argv):
    if len(argv) < 2:
        if os.path.isfile('.bobcatAnalyzer.rc'):
            with open('.bobcatAnalyzer.rc') as f:
                IP = f.readline().rstrip()
        else:
            print("Usage: ./bobcatLogAnalyzer.py IP_ADDRESS")
            exit(1)
    else:
        IP = argv[1]
    url = 'http://' + IP + '/log/console.log'
    res = requests.get(url, auth=HTTPBasicAuth('bobcat', 'miner'))
    for line in res.iter_lines():
#        print(line.decode("ascii"))
        parse_line(line.decode("ascii"))



if __name__ == '__main__':
    main(sys.argv)
