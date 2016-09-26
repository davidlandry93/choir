#!/bin/bash

for ip in 192.168.0.{101,102,104,105,106,114}
do
    ssh -t robmob@${ip} "python3 $HOME/choir/signer_server.py"
done
