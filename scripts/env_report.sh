#!/bin/bash

os_name=$(grep PRETTY_NAME /etc/os-release | cut -d'"' -f2)
kernel=$(uname -r)
cpu=$(nproc)

echo "OS:    $os_name"
echo "Krnel: $kernel"
echo "CPU:   $cpu"
