#cd /opt/pwd
pip install -r requirements.txt
./ctime_blank_unittest.py
./ctime_button_unittest.py
./ctime_common_unittest.py
/home/appuser/.local/bin/coverage run -m unittest ctime_blank_unittest.py
/home/appuser/.local/bin/coverage xml
rm -rf __pycache__
