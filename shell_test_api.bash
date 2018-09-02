#!/usr/bin/env bash

# create a new request and store the id
REQ_ID=$(curl localhost:5000/new 2>/dev/null| jq -r '.request_id' )
echo "request ${REQ_ID} created"

# use the id to get the details
curl localhost:5000/${REQ_ID} 2>/dev/null

# use the id to say the car for the request is at at the pickup point
curl -s localhost:5000/arrived_at_pickup/${REQ_ID} > /dev/null

# use the id to get the details - note that state has changed
echo
echo 'note that is_car_arrived_at_pickup is now true'
curl localhost:5000/${REQ_ID}

# use the id to say the car for the request is at at the dropoff point
curl -s localhost:5000/arrived_at_dropoff/${REQ_ID} >/dev/null

# use the id to get the details - note that state has changed
echo
echo 'note that is_car_arrived_at_dropoff is now true'
curl  localhost:5000/${REQ_ID}

