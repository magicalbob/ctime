cd /opt/pwd
pip install -r requirements.txt
./ctime_blank_unittest.py
coverage run -m unittest ctime_blank_unittest.py
coverage xml
rm -rf __pycache__
