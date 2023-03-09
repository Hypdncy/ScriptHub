#! /usr/bin/env bash

# set -x

id=$(xinput | grep "Touchpad" | awk -F '[ \t]+' '{for (i=1;i<NF;i++) if ($i~/id=/) print substr($i,4) }')

if [ -z "$id" ]; then
    echo "not find id of Touchpad"
elif [ "$1" == "disable" ]; then
    xinput --disable "$id"
    echo "Touchpad is disable"
elif [ "$1" == "enable" ]; then
    xinput --enable "$id"
    echo "Touchpad is enable"
fi
