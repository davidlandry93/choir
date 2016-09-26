#!/bin/bash

for ip in 192.168.0.{100..112}
do
    ssh -c "curl  -sSf" | sh  robmob@ip
done

