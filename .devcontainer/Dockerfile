FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install any additional packages you might need
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up any environment variables if needed
ENV DEBIAN_FRONTEND=noninteractive

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Check if the user already exists, and if not, create it
RUN if ! id -u $USERNAME > /dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME \
        && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi

# Set the default user
USER $USERNAME

# Set up Python virtual environment
RUN python3 -m venv /home/$USERNAME/venv
ENV PATH="/home/$USERNAME/venv/bin:$PATH"

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog