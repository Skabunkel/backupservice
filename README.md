# backupservice
A backup service that monitor and syncs directories/files to diffrent targets.

## Requirements

* Python 3

## Setup

### pipenv
If you are using ´pipenv´ just run this command in the projects folder.
```
pipenv install
```

### using regular pip or other python helper
You can just use pip to install the requirements. 
```
pip3 install -r requirements.txt
```

## Idea.

This services will according to some schedule sync files to some backup solution,
 based on some experience and ~~some level of auti~~ feeling i want something like the following.

Currently it feels like yaml will be a good choice because we want to use ansible, and this syntax would be related,
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
