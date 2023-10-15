#!/usr/bin/env bash
sudo wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip
sudo unzip sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip
sudo mv sonar-scanner-${SONAR_SCANNER_VERSION}-linux/ /opt/sonar-scanner
sudo ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner
