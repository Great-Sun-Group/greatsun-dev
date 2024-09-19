FROM mcr.microsoft.com/devcontainers/python:3

# Copy the startup script
COPY startup.sh /usr/local/bin/startup.sh

# Make the startup script executable
RUN chmod +x /usr/local/bin/startup.sh

# Run the startup script during build
RUN /usr/local/bin/startup.sh

# Set the entrypoint to run bash
ENTRYPOINT ["/bin/bash"]