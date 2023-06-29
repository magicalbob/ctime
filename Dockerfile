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
COPY requirements.txt /home/appuser/requirements.txt
COPY testscript.sh /home/appuser/testscript.sh
COPY ctime_blank.py /home/appuser/ctime_blank.py
COPY ctime_blank_unittest.py /home/appuser/ctime_blank_unittest.py
COPY ctime_button.py /home/appuser/ctime_button.py
COPY ctime_button_unittest.py /home/appuser/ctime_button_unittest.py
COPY ctime_common.py /home/appuser/ctime_common.py
COPY ctime_common_unittest.py /home/appuser/ctime_common_unittest.py
COPY ctime_camera.py /home/appuser/ctime_camera.py
COPY ctime_camera_unittest.py /home/appuser/ctime_camera_unittest.py

# Change the ownership of the testscript.sh file to the new user
RUN chown appuser:appuser /home/appuser/testscript.sh

# Switch to the new user
USER appuser

# Set the working directory to the new user's home directory
WORKDIR /home/appuser

# Install coverage
RUN pip install coverage

# Run the script as the new user
CMD sh -c ./testscript.sh
