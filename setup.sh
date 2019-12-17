#?/bin/bash

sudo apt-get install -y virtualenv nginx
pip install -r requirements.txt
sudo python config.py
