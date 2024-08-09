#cd /opt/pwd
pip install -r requirements.txt
~/.local/bin/coverage run -m unittest $(find src -name '*\.py'|grep -v 'test.py')
~/.local/bin/coverage xml
rm -rf __pycache__
