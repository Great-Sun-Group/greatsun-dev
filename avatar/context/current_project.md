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
   - Monitor the production environment for any issues or errors after deployment.