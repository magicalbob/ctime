# Use the almalinux:9 image as the base
FROM almalinux:9

# Install necessary packages
RUN dnf update -y \
 && dnf install -y python3-pip python3-devel alsa-lib-devel \
 && dnf groupinstall -y 'Development Tools'

# Create a new user named 'appuser'
RUN groupadd -g 1002 appuser \
 && useradd -ms /bin/bash -u 1001 -g 1002 appuser

# Copy the testscript.sh file into the appuser's home directory
COPY testscript.sh /home/appuser/testscript.sh
COPY testscript_docker.sh /home/appuser/testscript_docker.sh

# Change the ownership of the testscript.sh file to the new user
RUN chown appuser:appuser /home/appuser/testscript.sh

# Switch to the new user
USER appuser

# Set the working directory to the new user's home directory
WORKDIR /home/appuser

# Install coverage
RUN pip install coverage

# Run the script as the new user
CMD sh -c ./testscript_docker.sh
