rm -rf __pycache__
docker run -e SONAR_HOST_URL="https://sonarqube.ellisbs.co.uk" -e SONAR_LOGIN="sqp_b4a30f72a01b53da17b073fc8173515f56c57942" -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli
