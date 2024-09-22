# Current Project

Finish setting up the greatsun-dev environment while releasing production ready mvps of credex-core and vimbiso-pay by 4am Atlantic time on Monday, in 12 hours.

## Overview
The greatsun-dev environment is designed to facilitate rapid testing and deployment of credex-core and credex-bot. This setup aims to streamline the development and deployment of these services.

## Current State
Greatsun-dev is running but not fully complete, and the clients are well built and tested, but have not yet connected together over the api since significant security upgrades.

## Operational Pipeline

- Finish the core functionality of the greatsun-dev avatar: `engage`, `deploy stage`, `deploy prod`.
- Hands-on confirmation that credex-core api is secure and responding to authorized calls.
- Hands-on confirmation that vimbiso-pay is working as expected and processing reponses from the API appropriately.
#### up to here required by 4am Atlantic

- Finish the core functionality of the greatsun-dev avatar with: `stepback`
- fix commit errors when branch doesn't exist in some repos.
- add avatar clear and make avatar up more forgiving.
- Auto-deploy for prod in the DCO.
- Unit tests, integration tests, security tests
- Extended transaction modeling and performance tests.
- Web portal for customer service agents.
- System dashboard to monitor activity and process alerts.
- Initial data visualization and analytics.
- Build out CI/CD pipeline
- Add an avatar-generated summary of every merge to project and merge to dev based on the diff.


# Recommended Plan

1. **Finish the core functionality of the greatsun-dev avatar**
   - Implement the `avatar engage` command to start the submodule servers in development mode.

2. **Secure and test credex-core API**
   - Review and implement any necessary security upgrades to the credex-core API.
   - Ensure that the API is responding to authorized calls from vimbiso-pay and other clients.
   - Write and run comprehensive unit tests and integration tests for the API.
   - Perform security testing (e.g., penetration testing, vulnerability scanning) on the API.

3. **Test and integrate vimbiso-pay with credex-core API**
   - Update vimbiso-pay to integrate with the latest version of the credex-core API.
   - Test the end-to-end flow of vimbiso-pay interacting with the API (e.g., sending requests, receiving responses, processing transactions).
   - Perform load testing and stress testing on vimbiso-pay to ensure it can handle expected traffic and usage patterns.
   - Conduct user acceptance testing (UAT) with a small group of users to identify and resolve any issues.

4. **Final testing and deployment (5 hours)**
   - Perform final integration testing between credex-core and vimbiso-pay in a staging environment.
   - Address any remaining issues or bugs identified during testing.
   - Deploy the production-ready MVPs of credex-core and vimbiso-pay to the production environment.
   - Monitor the production environment for any issues or errors after deployment.## Starting the credex-core Submodule

To start the credex-core submodule within the greatsun-dev environment, follow these steps:

1. **Build the Docker image**
   - Navigate to the `credex-ecosystem/credex-core` directory.
   - Run the following command to build the Docker image:
     ```
     docker build -t credex-core .
     ```

2. **Remove existing containers (if any)**
   - List all running containers:
     ```
     docker ps
     ```
   - Stop the `credex-core` container (if running):
     ```
     docker stop credex-core
     ```
   - Remove the `credex-core` container:
     ```
     docker rm credex-core
     ```

3. **Run the Docker container**
   - Use the following command to run the credex-core container:
     ```
     docker run -p 5000:5000 --env NODE_ENV=production --env-file <(env | grep -v ' ') --name credex-core credex-core
     ```
   - This command will:
     - Run the `credex-core` Docker image.
     - Map the container's port 5000 to the host's port 5000.
     - Set the `NODE_ENV` environment variable to `production`.
     - Pass all the environment variables from the greatsun-dev container (except those with spaces) to the credex-core container.
     - Assign the name `credex-core` to the container.

4. **Verify the credex-core API**
   - Once the container is up and running, you can check if the credex-core API is accessible by sending a request to `http://localhost:5000` using a tool like `curl` or a web browser:
     ```
     curl http://localhost:5000
     ```
   - If the API is running correctly, you should receive a response indicating that the credex-core API is up and running.

By following these steps, you can ensure that the credex-core submodule is started and running within the greatsun-dev environment whenever needed.