#!/usr/bin/env python3

import argparse
import os
import requests
import json
import sys

parser = argparse.ArgumentParser(description='Download state files from Scalr')
parser.add_argument('--output-dir', '-o', type=str, help='Output directory')
parser.add_argument('--host', '-d', type=str, help='Scalr host')
parser.add_argument('--token', '-t', type=str, help='Scalr API token')
args = parser.parse_args()

output_dir = args.output_dir
host = args.host or os.environ.get('SCALR_HOST')
token = args.token or os.environ.get('SCALR_TOKEN')

if not all([output_dir, host, token]):
    parser.print_help()
    sys.exit(1)

headers = {
    "accept": "application/vnd.api+json",
    "Prefer": "profile=preview",
    "authorization": "Bearer " + token
}

page = 1

while True:

    url = "https://" + host + "/api/iacp/v3/workspaces?page[number]=" + str(page)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Request failed. Wrong token?")
        sys.exit(1)

    data = json.loads(response.text)

    total_pages = data['meta']['pagination']['total-pages']

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for item in data['data']:

        url = "https://" + host + "/api/iacp/v3/workspaces/" + item['id'] + "/current-state-version"

        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        try:
            download_link = data['data']['links']['download']
        except KeyError:
            continue

        print("Downloading state file for " + item['id'] + " to " + output_dir)

        response = requests.get(download_link)
        with open(output_dir + "/" + item['id'] + ".json", "wb") as f:
            f.write(response.content)

    if page == total_pages:
        sys.exit(0)

    page += 1
