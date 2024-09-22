#!/bin/bash

if [ "$1" = "up" ]; then
    python3 /workspaces/greatsun-dev/avatar/utils/avatarUp.py
else
    echo "Usage: avatar up"
fi