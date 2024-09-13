#!/bin/bash

# Function to start a service
start_service() {
    local service_name=$1
    local start_command=$2
    local log_file="/workspaces/credex-dev/${service_name}.log"

    echo "Starting ${service_name}..."
    cd "/workspaces/credex-dev/${service_name}"
    eval "${start_command} > ${log_file} 2>&1 &"
}

# Start credex-core
start_service "credex-core" "npm run dev"

# Start credex-bot
start_service "credex-bot" "python main.py"

# Start credex-dev
start_service "credex-dev" "python main.py"

# Wait for services to start
timeout=60
start_time=$(date +%s)
while true; do
    if grep -q "Server is running" "/workspaces/credex-dev/credex-core.log" && \
       grep -q "Bot is running" "/workspaces/credex-dev/credex-bot.log" && \
       grep -q "Credex-dev is running" "/workspaces/credex-dev/credex-dev.log"; then
        echo "All services started successfully!"
        break
    fi

    current_time=$(date +%s)
    if [ $((current_time - start_time)) -ge $timeout ]; then
        echo "Timeout: One or more services failed to start within ${timeout} seconds."
        echo "credex-core log:"
        tail -n 20 /workspaces/credex-dev/credex-core.log
        echo "credex-bot log:"
        tail -n 20 /workspaces/credex-dev/credex-bot.log
        echo "credex-dev log:"
        tail -n 20 /workspaces/credex-dev/credex-dev.log
        exit 1
    fi

    sleep 1
done

# Keep the script running and tail the log files
tail -f /workspaces/credex-dev/credex-core.log /workspaces/credex-dev/credex-bot.log /workspaces/credex-dev/credex-dev.log