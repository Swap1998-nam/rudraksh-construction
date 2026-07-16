** **
clone repo to linux machine 

Then on the Linux server run these commands:

cd /home/ubuntu/rudraksh-construction
apt install python3.14-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed.py
python run.py

