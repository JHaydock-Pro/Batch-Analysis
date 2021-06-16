import argparse
import json
import os
import pandas as pd
import requests
from datetime import datetime

def get_hosts(url):
    response = requests.get(url).json()
    hosts = {}

    for i in response[""]:
        for j in response[""][i]:
            for k in response[""][i][j]:

                hosts[k] = {
                    "trance": i
                }

                if response[""][i][j][k]["nagios"] != " ":
                    hosts[k]["status"] = response[""][i][j][k]["nagios"].strip()
                else:
                    hosts[k]["status"] = "ok"

                if "note" in response[""][i][j][k]:
                    hosts[k]["note"] = response[""][i][j][k]["note"]
                else:
                    hosts[k]["note"] = None

    return hosts

def get_hosts_by_status(url, status, ignore_downtime, ignore_notes):
    matches={}
    hosts = get_hosts(url)
    for host in hosts:
        if (
            # Include if status matches
            status.lower() in hosts[host]["status"]
            # Don't include hosts with downtime if ignore_downtime is True
            and not (ignore_downtime and "downtime" in hosts[host]["status"])
            # Don't include hosts with notes if ignore_notes is True
            and not (ignore_notes and hosts[host]["note"] != None)
        ):
            matches[host] = hosts[host]
    return matches

def get_aq_info(hosts, aq_url):
    response = requests.get(aq_url).json()

    for host in hosts:
        #TODO - Filter out redundant information and wrap in try/except
        if host in response.keys():
            hosts[host].update(response[host])
    return hosts

def get_host_info(args):
    hosts = {}
    for status in args.status.split(','):
        hosts_by_status = get_hosts_by_status(args.url, status, args.ignore_downtime, args.ignore_notes)
        hosts.update(hosts_by_status)
    hosts_aq = get_aq_info(hosts, args.aq_url)
    return hosts_aq

def output_to_json(hosts):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    now = datetime.now()
    filename = os.path.join('logs', now.strftime('WN_Log_%Y_%m_%d_%H_%M.json'))

    with open(filename, 'w') as outfile:
        json.dump(hosts, outfile)

def output_to_stdout(hosts):
    values = []
    for host in hosts:
        row = []
        row.append(host)
        row.append(hosts[host]['ip'])
        row.append(hosts[host]['trance'])
        row.append(hosts[host]['archetype'])
        row.append(hosts[host]['personality'])
        row.append(hosts[host]['status'])
        row.append(hosts[host]['note'])
        values.append(row)
    pd.set_option('display.width', 0)
    df = pd.DataFrame(values, columns=[
        "Host",
        "IP",
        "Trance",
        "Archetype",
        "Personality",
        "Status",
        "Note"
        ])
    df.style.set_properties(**{'text-align': 'left'})
    print(df)

parser = argparse.ArgumentParser()
parser.add_argument(
    '-u', '--url',
    help="URL to get hosts from.",
    action='store',
    dest='url',
    default='http://mimic.gridpp.rl.ac.uk/views/view-logical-workers.php'
    )
parser.add_argument(
    '-a', '--aqurl',
    help="URL to get extra host info from Aquilon.",
    action='store',
    dest='aq_url',
    default='http://aquilon.gridpp.rl.ac.uk/cgi-bin/report/host_personality_branch'
    )
parser.add_argument(
    '-s', '--status',
    help="Status of hosts to log. Default: critical",
    action='store',
    dest='status',
    default='critical'
    )
parser.add_argument(
    '-d', '--ignore-downtime',
    help="Ignore hosts that are in downtime.",
    action='store_true',
    dest='ignore_downtime',
    default = False
    )
parser.add_argument(
    '-n', '--ignore-notes',
    help="Ignore hosts that have notes in mimic.",
    action='store_true',
    dest='ignore_notes',
    default = False
    )
parser.add_argument(
    '-j', '--json',
    help="Export output to json file.",
    action='store_true',
    dest='json'
    )
parser.add_argument(
    '-c', '--stdout',
    help="Export output to console stdout as table.",
    action='store_true',
    dest='stdout'
    )
args = parser.parse_args()

hosts = get_host_info(args)
if args.json:
    output_to_json(hosts)
if args.stdout:
    output_to_stdout(hosts)
