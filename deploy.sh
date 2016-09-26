#!/bin/bash

for ip in 192.168.0.{102,106}
do
    ssh -t robmob@${ip} "curl https://raw.githubusercontent.com/davidlandry93/choir/master/deploy_server.sh -sSf | sh"
done

