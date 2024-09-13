FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

# Install any additional packages you might need
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up any environment variables if needed
ENV DEBIAN_FRONTEND=noninteractive

# Any additional setup or configurations can be added here

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog