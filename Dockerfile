FROM mcr.microsoft.com/devcontainers/python:3

# Copy the startup script
COPY startup.sh /usr/local/bin/startup.sh

# Make the startup script executable
RUN chmod +x /usr/local/bin/startup.sh

# Run the startup script when the container starts
CMD ["/bin/bash", "-c", "/usr/local/bin/startup.sh && /bin/bash"]