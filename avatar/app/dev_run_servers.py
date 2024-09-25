import os
import subprocess

# needs to use config variables for paths, modules, etc


def dev_run_servers():

    # Remove any existing containers with the names "credex-core" or "vimbiso-pay"

    try:
        # Get all container IDs
        containers = subprocess.check_output(
            ['docker', 'ps', '-q', '-a'], stderr=subprocess.DEVNULL).decode().strip().split('\n')

        for container in containers:
            if container:  # Check if container ID is not empty
                try:
                    # Get container name
                    container_name = subprocess.check_output(
                        ['docker', 'inspect', '--format',
                            '{{.Name}}', container],
                        stderr=subprocess.DEVNULL
                    ).decode().strip()

                    # Check if it's one of the containers we want to remove
                    if 'credex-core' in container_name or 'vimbiso-pay' in container_name:
                        try:
                            subprocess.run(
                                ['docker', 'rm', '-f', container], check=True, stderr=subprocess.DEVNULL)
                            print(f"Successfully removed container: {
                                container_name}")
                        except subprocess.CalledProcessError:
                            print(f"Failed to remove container: {
                                container_name}")
                except subprocess.CalledProcessError:
                    print(
                        f"Failed to inspect container with ID: {container}")
    except subprocess.CalledProcessError:
        print(
            "Failed to list Docker containers. Proceeding with the rest of the script.")

    # Fire up credex-core
    os.chdir('/workspaces/greatsun-dev/credex-ecosystem/credex-core')
    subprocess.run(['docker', 'build', '-t', 'credex-core', '.'], check=True)
    env_vars = subprocess.check_output(
        "env | grep -v ' '", shell=True).decode('utf-8')
    docker_run_cmd = [
        'docker', 'run',
        '-d',  # Run in detached mode
        '-p', '5000:5000',
        '--env', f'NODE_ENV=development',
        '--env-file', '/dev/stdin',
        '--name', 'credex-core',
        'credex-core'
    ]
    subprocess.run(docker_run_cmd, input=env_vars.encode(), check=True)

    # Fire up vimbiso-pay
    os.chdir('/workspaces/greatsun-dev/credex-ecosystem/vimbiso-pay')
    subprocess.run(['docker', 'build', '-t', 'vimbiso-pay', '.'], check=True)
    env_vars = "DJANGO_SETTINGS_MODULE=config.development\n"
    env_vars += subprocess.check_output("env | grep -v ' '",
                                        shell=True).decode('utf-8')
    docker_run_cmd = [
        'docker', 'run',
        '-d',  # Run in detached mode
        '-p', '8000:8000',
        '--env-file', '/dev/stdin',
        '--name', 'vimbiso-pay',
        'vimbiso-pay',
        'sh', '-c',
        "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    ]
    subprocess.run(docker_run_cmd, input=env_vars.encode(), check=True)

    print("credex ecosystem online in greatsun-dev")
