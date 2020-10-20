# backupservice
A backup service that montores and syncs directories to diffrent targets.

This services will according to some schedule sync files to some backup solution,
 based on some experience and ~~some level of auti~~ feeling i want something like the following.

Currently it looks like yml will be a good choice because we use ansible, and this syntax would be related,
 and because ini files are shit for storing lists; it's a key value file format lets not get creative.

*config.yml*
```yaml

url: backup.int.studentnatet.se
schedule: */30 * * * *
jobs:
 - name: Syncing system configs # Syncs configs to default location.
   schedule: 0 */24 * * *
   targets:
    - "/etc/nginx/conf.d"
    - "/srv/magic"
 
 - name: Sync cheese stash # Syncs the cheese stash to a diffrent host using the default schedule.
   url: "cheese.studentnatet.se"
   targets:
    - "/home/wizard/cheese"

```
