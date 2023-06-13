rm -rf __pycache__
docker run -e SONAR_HOST_URL="https://sonarqube.ellisbs.co.uk" -e SONAR_LOGIN="${SONARQUBE_TOKEN}" -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli
