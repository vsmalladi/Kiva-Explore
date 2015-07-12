#!/usr/bin/env python2
# -*- coding: latin-1 -*-
'''GET list of all Teams from Kiva.org'''

import requests, json
import csv
import codecs

# Force return from the server in JSON format
HEADERS = {'accept': 'application/json'}

# This base URL searchs for teams on Kiva.org
URL = "http://api.kivaws.org/v1/teams/search.json"

# GET the base URL
response = requests.get(URL, headers=HEADERS)

# Extract the JSON response as a python dict
response_json_dict = response.json()

# Extract the number of pages
pages = response_json_dict["paging"]["pages"] 

# Iterate through all the pages and makes list of teams
teams = []
for i in range(1,pages+1):
    print "working on " + str(i)
    URL_page = URL + "?page=" + str(i)
    response = requests.get(URL_page, headers=HEADERS)
    response_json_dict = response.json()
    teams.extend(response_json_dict["teams"])

# Extract all the keys
keys = {}
for i in teams:
    for k in i.keys():
        keys[k] = 1

# Print the list into CSV file
with open('teams.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=keys)
    writer.writeheader()
    print len(teams)
    for row in teams:
        writer.writerow(dict((k, v.encode('utf-8') if type(v) is unicode else v) for k, v in row.iteritems()))
