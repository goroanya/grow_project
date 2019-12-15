#?/bin/bash

rm -rf venv
sudo apt-get install -y virtualenv nginx
virtualenv -p python3.8 venv
pip install -r requirements.txt
sudo python config.py
