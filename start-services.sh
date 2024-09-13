#!/bin/bash

# Start credex-core
echo "Starting credex-core..."
cd /workspaces/credex-dev/credex-core
npm run dev > /workspaces/credex-dev/credex-core.log 2>&1 &

# Start credex-bot
echo "Starting credex-bot..."
cd /workspaces/credex-dev/credex-bot
python main.py > /workspaces/credex-dev/credex-bot.log 2>&1 &

# Start credex-dev
echo "Starting credex-dev..."
cd /workspaces/credex-dev
python main.py > /workspaces/credex-dev/credex-dev.log 2>&1 &

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