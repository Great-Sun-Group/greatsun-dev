#!/bin/bash

# Function to start a service
start_service() {
    local service_name=$1
    local start_command=$2
    local log_file="/workspaces/credex-dev/${service_name}.log"

    echo "Starting ${service_name}..."
    if [ -d "/workspaces/credex-dev/${service_name}" ]; then
        cd "/workspaces/credex-dev/${service_name}"
        eval "${start_command} > ${log_file} 2>&1 &"
    else
        echo "Warning: ${service_name} directory not found. Skipping."
    fi
}

# Start credex-core
start_service "credex-core" "npm run dev"

# Start credex-bot
cd /workspaces/credex-dev/credex-bot
source venv/bin/activate
start_service "credex-bot" "python app/manage.py runserver 0.0.0.0:8000"
deactivate

# Start credex-dev (main script in the root directory)
echo "Starting credex-dev..."
cd /workspaces/credex-dev
python main.py > /workspaces/credex-dev/credex-dev.log 2>&1 &

# Wait for services to start
timeout=60
start_time=$(date +%s)
while true; do
    if grep -q "Starting development server" "/workspaces/credex-dev/credex-core.log" && \
       grep -q "Starting development server at http://0.0.0.0:8000/" "/workspaces/credex-dev/credex-bot.log" && \
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