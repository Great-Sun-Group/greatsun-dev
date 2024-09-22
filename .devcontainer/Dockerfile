FROM mcr.microsoft.com/devcontainers/python:3

# Copy the avatar command script and make the avatar command executable
COPY avatar/utils/avatar_command.sh /usr/local/bin/avatar
RUN chmod +x /usr/local/bin/avatar

# Set the entrypoint to run bash
ENTRYPOINT ["/bin/bash"]