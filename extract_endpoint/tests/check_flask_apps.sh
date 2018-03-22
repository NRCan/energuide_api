#!/bin/bash
TIMEOUT=0
ENDPOINT_RESULT=$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5000)
echo 'Checking that endpoint app is running'
until [ $ENDPOINT_RESULT -eq 200 ]; do
    echo 'endpoint is not running'
    sleep 5
    let TIMEOUT=TIMEOUT+1
    if [ $TIMEOUT -eq 10 ]; then
        echo 'process timed out, endpoint app is not running'
        echo 'exiting tests'
        exit 1
    fi
    ENDPOINT_RESULT=$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5000)
done
echo 'Endpoint app running successfully'

TIMEOUT=0
ETL_RESULT=$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5010)
echo 'Check that etl app is running'
until [ $ETL_RESULT -eq 200 ]; do
    echo 'etl app is not running'
    sleep 5
    let TIMEOUT=TIMEOUT+1
    if [ $TIMEOUT -eq 10 ]; then
        echo 'process timed out, etl app is not running'
        echo 'exiting tests'
        exit 1
    fi
    ETL_RESULT=$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5010)
done
echo 'etl app running successfully'
