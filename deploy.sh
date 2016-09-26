#!/bin/bash

for ip in 192.168.0.{101,102,104,105,106,114}
do
    ssh -t robmob@${ip} "curl https://raw.githubusercontent.com/davidlandry93/choir/master/deploy_server.sh -sSf | sh"
done

