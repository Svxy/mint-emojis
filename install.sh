#!/bin/bash

if ! command -v python3.10 &> /dev/null
then
    echo "Python 3.10 is required to run this app. It will be installed in 5 seconds.\n\nPress Ctrl+C to cancel."
    sleep 5

    sudo apt-get update
    sudo apt-get install python3.10
fi

echo "Installing Required Modules"
cd "$(dirname "$0")"
if [ "$(basename "$PWD")" != "Mint Emojis" ]; then
    echo "Please make sure this bash script is in the 'Mint Emojis' folder."
    sleep 5
else
    pip install -r requirements.txt
    echo "Completed.\n\nYou can now run Mint Emojis!"
fi

sleep 3