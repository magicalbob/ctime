#cd /opt/pwd
pip install -r requirements.txt
~/.local/bin/coverage run -m unittest ./src/ctime/ctime_button_unittest.py
~/.local/bin/coverage run -m unittest ./src/ctime/ctime_common_unittest.py
~/.local/bin/coverage run -m unittest ./src/ctime/ctime_blank_unittest.py
~/.local/bin/coverage xml
rm -rf __pycache__
