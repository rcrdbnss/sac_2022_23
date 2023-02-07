export TOPIC=wine_orders

export TOKEN="zxcvtoken"

export SUBSCRIPTION_NAME=wine_orders_sub

gcloud pubsub topics create ${TOPIC}

gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME} --topic ${TOPIC} --push-endpoint \
"https://${PROJECT_ID}.appspot.com/pubsub/push?token=${TOKEN}" --ack-deadline=10
