#!/bin/bash

name=$1

cd mac_authentication

if [ $name = "alice" ]
then
    python3 alice.py
elif [ $name = "bob" ]
then
    python3 bob.py
else
    echo "No valid argument given (alice/bob)."
fi
