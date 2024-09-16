#!/bin/bash

# Function to start a service
start_service() {
    local service_name=$1
    local start_command=$2
    local log_file="/workspaces/greatsun-dev/${service_name}.log"

    echo "Starting ${service_name}..."
    if [ -d "/workspaces/greatsun-dev/${service_name}" ]; then
        cd "/workspaces/greatsun-dev/${service_name}"
        eval "${start_command} > ${log_file} 2>&1 &"
    else
        echo "Warning: ${service_name} directory not found. Skipping."
    fi
}

echo "Starting greatsun-dev..."
cd /workspaces/greatsun-dev
python main.py > /workspaces/greatsun-dev/greatsun-dev.log 2>&1 &

echo "Starting credex-core..."
cd /workspaces/greatsun-dev/credex-core
start_service "credex-core" "npm run dev"

echo "Starting vimbiso-pay..."
cd /workspaces/greatsun-dev/vimbiso-pay
source venv/bin/activate
start_service "vimbiso-pay" "python app/manage.py runserver 0.0.0.0:8000"
deactivate

cd /workspaces/greatsun-dev

# Wait for services to start
timeout=60
start_time=$(date +%s)
while true; do
    if grep -q "Starting development server" "/workspaces/greatsun-dev/credex-core.log" && \
       grep -q "Starting development server at http://0.0.0.0:8000/" "/workspaces/greatsun-dev/vimbiso-pay.log" && \
       grep -q "vimbiso-pay is running" "/workspaces/greatsun-dev/greatsun-dev.log"; then
        echo "All services started successfully!"
        break
    fi

    current_time=$(date +%s)
    if [ $((current_time - start_time)) -ge $timeout ]; then
        echo "Timeout: One or more services failed to start within ${timeout} seconds."
        echo "credex-core log:"
        tail -n 20 /workspaces/greatsun-dev/credex-core.log
        echo "vimbiso-pay log:"
        tail -n 20 /workspaces/greatsun-dev/vimbiso-pay.log
        echo "greatsun-dev log:"
        tail -n 20 /workspaces/greatsun-dev/greatsun-dev.log
        exit 1
    fi

    sleep 1
done

# Keep the script running and tail the log files
tail -f /workspaces/greatsun-dev/central-logs/credex-core.log /workspaces/greatsun-dev/central-logs/vimbiso-pay.log /workspaces/greatsun-dev/central-logs/greatsun-dev.log