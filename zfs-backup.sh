#!/bin/bash

DATE=$(date '+%Y-%m-%d') # Date format, used for naming.

SSD_SNAP=10 # How many snapshots to store on hot.
HDD_SNAP=60 # How many copies to store on cold storage.

SRC="pool"  # The source pool to copy from, also known as hot storage.
DEST="backup" # The source pool to copy to, also known as cold storage.

HOT=true

mapfile -t FOLDERS < <(zfs list -r $SRC -o name | grep "$SRC/")

get_snaps() {
  local TODAYS_SNAP="$1@$2"
  mapfile -t SNAPS < <(zfs list -H -t snapshot -r "$1" -o name -s creation)

  if [ "$3" = true ]; then
    if [[ ! "${SNAPS[@]}" =~ "${TODAYS_SNAP}" ]]; then
      zfs snapshot "$TODAYS_SNAP"
      SNAPS+=("$TODAYS_SNAP")
    fi
  fi
}

for FOLDER in "${FOLDERS[@]}"
do
  echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Starting ZFS backup."
  declare -a SNAPS
  get_snaps "$FOLDER" "$DATE" "$HOT"

  DEST_FOLDER="${FOLDER/$SRC/$DEST}"
  mapfile -t DEST_SNAPS < <(zfs list -H -t snapshot -r "$DEST_FOLDER" -o name -s creation)

  declare -a LAST_SNAP
  if [ "${#DEST_SNAPS[@]}" -lt "1" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Force pushing new dataset ${SNAPS[0]}."
    zfs send "${SNAPS[0]}" | zfs recv -F "$DEST_FOLDER"
  else
    LAST_SNAP="${DEST_SNAPS[${#DEST_SNAPS[@]}-1]/$DEST/$SRC}"
    echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Sending snapshots."

    if [ "${#SNAPS[@]}" -gt "1" ]; then
      if [[ "${SNAPS[${#SNAPS[@]}-1]}" != "${LAST_SNAP}"  ]]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Trying incremental send from $LAST_SNAP ro ${SNAPS[${#SNAPS[@]}-1]}."
        zfs send -i "$LAST_SNAP" "${SNAPS[${#SNAPS[@]}-1]}" | zfs recv "$DEST_FOLDER" || zfs send "${SNAPS[${#SNAPS[@]}-1]}" | zfs recv -F "$DEST_FOLDER"
      fi
    else
      if [[ "${SNAPS[0]}" != "${LAST_SNAP}"  ]]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Force pushing new dataset ${SNAPS[0]}."
        zfs send "${SNAPS[0]}" | zfs recv -F "$DEST_FOLDER"
      fi
    fi
  fi

  echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Removing old HDD snapshots."
  while [ "${#DEST_SNAPS[@]}" -gt "$HDD_SNAP" ]
  do
    echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Removing snapshot \"${DEST_SNAPS[0]}\"."

    zfs destroy "${DEST_SNAPS[0]}"
    unset DEST_SNAPS[0]
  done

  echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Removing old SSD snapshots."
  while [ "${#SNAPS[@]}" -gt "$SSD_SNAP" ]
  do
    echo "$(date '+%Y-%m-%d %H:%M:%S.%3N') - $FOLDER - Removing snapshot \"${SNAPS[0]}\"."

    zfs destroy "${SNAPS[0]}"
    unset SNAPS[0]
  done
done
