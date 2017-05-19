#!/usr/bin/env python3

import sys
import gen
import requests
import time

def assault(host):
    reqs = 0
    time_old = time.time()
    reqs_old = 0

    session = requests.Session()

    while True:
        trade = gen.generate_fx()
        session.post(host, data=trade.encode('utf-8'))
        reqs = reqs + 1
        if time.time() - time_old > 2:
            rps = int((reqs - reqs_old) / (time.time() - time_old))
            print("rps: ", rps)
            reqs_old = reqs
            time_old = time.time()

def usage():
    print("assault.py host")
    os.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    host = sys.argv[1]

    assault(host)


if __name__ == '__main__':
    main()
