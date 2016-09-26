#!/bin/bash

for ip in 192.168.0.{101,102,104,105,106,109,111,114}
do
    echo "Starting ${ip}"
    ssh robmob@${ip} "nohup python3 /home/robmob/choir/singer_server.py &"
done

echo "Done."
