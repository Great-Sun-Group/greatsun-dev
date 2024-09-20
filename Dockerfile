FROM mcr.microsoft.com/devcontainers/python:3

# Copy the avatar command script
COPY avatar_command.sh /usr/local/bin/avatar

# Make the avatar command executable
RUN chmod +x /usr/local/bin/avatar

# Set the entrypoint to run bash
ENTRYPOINT ["/bin/bash"]