if [ "${CIRCLE_BRANCH}" == "slack_notification" ]; then
    curl -X POST --data-urlencode "payload={\"channel\": \"#circleci_test\", \"text\": \"@here Master is failing\"}" $NRCAN_SLACK_URL
fi
