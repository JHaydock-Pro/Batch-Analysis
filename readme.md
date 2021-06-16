# Batch Farm Analysis
Scans batch farm hosts based on status in mimic. Gathers some basic info for storage and later analysis regarding failure trends.

| Option | Default | Effect |
|--------|---------|--------|
| -u, --url | http://mimic.gridpp.rl.ac.uk/views/view-logical-workers.php | URL to get list of batch farm workers. |
| -a, --aqurl | http://aquilon.gridpp.rl.ac.uk/cgi-bin/report/host_personality_branch | URL to get extra information from Aquilon. |
| -s, --status | critical | Comma separated list of statuses of hosts to get info from. eg. critical, downtime, ok |
| -d, --ignore-downtime | | Set if any hosts with downtime should be ignored. (Recommended if searching for 'down' status.)  |
| -n, --ignore-notes | | Set if any hosts with notes in mimic should be ignored. |
| -j, --json | | Output results to json file in logs/ |
| -c, --stdout | | Output to console stdout as table. |


For example, the following will output a list of hosts to the command line that are currently down but have no notes or downtime set on them.
```
py batch_analysis.py -cdn -s critical,down
```
And running the following at regular intervals will create a number of json files in the `logs/` dir containing info about critical hosts that can be used for later visualisation and analysis.
```
py batch_analysis.py -j
```

---
## TODO
- Output data to long-term storage solution such as influxDB.
- Visualise data, or have something like grafana do it.
- Consider using AQ client to get even more useful information from Aquilon such as OS and rack.
