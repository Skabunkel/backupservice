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

url: 'backup.lan' # if its not defined it will default to localhost
user: 'backup' # if its not defined it will default to current user using the $USER enviroment variable
schedule: '*/30 * * * *'
to: '/data/{hostname}' #if its not defined it will default to tmp if {hostname} is defined it will replace it with current hostname.
jobs:
 - name: 'Syncing system configs' # Syncs configs to default location.
   schedule: '0 */24 * * *'
   targets:
    - '/etc/nginx/conf.d'
    - '/srv/magic'
 
 - name: 'Sync cheese stash' # Syncs the cheese stash to a diffrent host using the default schedule.
   user: 'wizard'
   url: 'cheese.lan'
   targets:
    - '/home/wizard/cheese'

 - name: 'Magic stash' # Syncs the 'Magic stash' to  a diffrent destination path.
   to: '/magic/stash'
   url: 'cheese.lan'
   targets: 
    - '/tmp/no'

```
