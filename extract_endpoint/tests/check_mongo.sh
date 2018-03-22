#!/bin/bash
TIMEOUT=0
RESULT=$(mongo energuide --eval 'db.dwellings.count()' --quiet)
until [  $RESULT -eq 7 ]; do
 echo 'mongo not populated'
 sleep 5
 let TIMEOUT=TIMEOUT+1
 if [ $TIMEOUT -eq 6 ]; then
    echo 'process timed out, mongo was not populated'
    echo 'exiting tests'
    exit 1
 fi
 RESULT=$(mongo energuide --eval 'db.dwellings.count()' --quiet)
done
echo 'mongo populated, continuing process'
