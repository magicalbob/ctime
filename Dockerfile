# Use the almalinux:9 image as the base
FROM almalinux:9

# Install necessary packages
RUN dnf update -y && \
    dnf install -y python3-pip

# Create a new user named 'appuser'
RUN useradd -ms /bin/bash appuser

# Copy the testscript.sh file into the appuser's home directory
COPY testscript.sh /home/appuser/testscript.sh

# Change the ownership of the testscript.sh file to the new user
RUN chown appuser:appuser /home/appuser/testscript.sh

# Switch to the new user
USER appuser

# Set the working directory to the new user's home directory
WORKDIR /home/appuser

# Run the script as the new user
CMD sh -c ./testscript.sh
