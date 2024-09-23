#!/bin/bash

# Start credex-core
echo "Starting credex-core..."
cd /workspaces/greatsun-dev/credex-ecosystem/credex-core
docker build -t credex-core .

# Run the `credex-core` Docker image.
# Map the container's port 5000 to the host's port 5000.
# Set the `NODE_ENV` environment variable to `development`.
# Pass all the environment variables from the greatsun-dev container (except those with spaces) to the credex-core container.
# Assign the name `credex-core` to the container.
docker run -p 5000:5000 --env NODE_ENV=development --env-file <(env | grep -v ' ') --name credex-core credex-core

# Start vimbiso-pay
#echo "Starting vimbiso-pay..."
#cd /workspaces/greatsun-dev/credex-ecosystem/vimbiso-pay
#python manage.py runserver &chmod +x start_submodules.sh

# Go back home
cd /workspaces/greatsun-dev
