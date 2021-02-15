#!/bin/bash

sleep 5

chown -R mongodb:mongodb /home/mongodb

gosu mongodb mongod --dbpath=/data/db --config mongod.conf --bind_ip_all --auth

nohup gosu mongodb mongo admin --eval "help" > /dev/null 2>&1
RET=$?

while [[ "$RET" -ne 0 ]]; do
  echo "Waiting for MongoDB to start..."
  mongo admin --eval "help" > /dev/null 2>&1
  RET=$?
  sleep 2
done

#gosu mongodb mongod --dbpath=/data/db --config mongod.conf --bind_ip_all --auth