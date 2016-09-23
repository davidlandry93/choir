#!/bin/bash

for ip in 192.168.0.{100..112}
do
    ssh-copy-id robmob@${ip}
done

