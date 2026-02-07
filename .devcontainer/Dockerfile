FROM mcr.microsoft.com/devcontainers/base:ubuntu

RUN apt-get update && apt-get install -y \
    gnupg2 \
    pinentry-tty \
    git \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Configure GPG for non-interactive use
RUN mkdir -p /home/vscode/.gnupg && \
    echo "pinentry-program /usr/bin/pinentry-tty" > /home/vscode/.gnupg/gpg-agent.conf && \
    echo "no-tty" > /home/vscode/.gnupg/gpg.conf && \
    chmod 700 /home/vscode/.gnupg && \
    chown -R vscode:vscode /home/vscode/.gnupg

# Copy init script into the image
COPY init-agent.sh /usr/local/bin/init-agent.sh
RUN chmod +x /usr/local/bin/init-agent.sh
