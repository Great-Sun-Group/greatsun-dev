#!/bin/bash

# Start credex-core
echo "Starting credex-core..."
cd /workspaces/greatsun-dev/credex-ecosystem/credex-core
docker-compose up -d

# Start vimbiso-pay
echo "Starting vimbiso-pay..."
cd /workspaces/greatsun-dev/credex-ecosystem/vimbiso-pay
python manage.py runserver &chmod +x start_submodules.sh