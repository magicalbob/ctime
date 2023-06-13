rm -rf __pycache__
docker build -t local:testctime .
docker run -v ${PWD}:/opt/pwd local:testctime
