#cd /opt/pwd
pip install -r requirements.txt
~/.local/bin/coverage run -m unittest discover -v -s src/ctime -p '*_test.py'
~/.local/bin/coverage xml
rm -rf __pycache__
