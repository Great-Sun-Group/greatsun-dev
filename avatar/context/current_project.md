# Current Project

Finish setting up the greatsun-dev environment while releasing production ready mvps of credex-core and vimbiso-pay by 4am Atlantic time on Monday, in 12 hours.

## Overview
The greatsun-dev environment is designed to facilitate rapid testing and deployment of credex-core and credex-bot. This setup aims to streamline the development and deployment of these services.

## Current State
Greatsun-dev is running but not fully complete, and the clients are well built and tested, but have not yet connected together over the api since significant security upgrades.

## Operational Pipeline

1. Hands-on confirmation that credex-core api is secure and responding to authorized calls.
2. Hands-on confirmation that vimbiso-pay is working as expected and processing reponses from the API appropriately.
3. Automated extended patterns of call to the whatsapp bot to test functionality across the system.


- Finish the core functionality of the greatsun-dev avatar
- fix commit errors when branch doesn't exist in some repos.
- Auto-deploy happens in prod in the DCO.
- Unit tests, integration tests, security tests
- Extended transaction modeling and performance tests.
- Web portal for customer service agents.
- System dashboard to monitor activity and process alerts.
- Initial data visualization and analytics.
- Build out CI/CD pipeline
- Add an avatar-generated summary of every merge to project and merge to dev based on the diff.


2. Test WhatsApp Simulation Interface
   - Thoroughly test the `simulate_user.py` script to ensure it accurately simulates WhatsApp interactions.
   - Verify that all types of messages (text, interactive, etc.) are handled correctly.
   - Test error handling and edge cases in the simulation.

3. Enhance Interactive Message Handling
   - Implement proper display and handling of interactive messages (e.g., buttons, list options).
   - Ensure that user responses to interactive messages are correctly processed.

# VimbisoPay Terminal Simulator Issues and Next Steps

## Current State
We are working on fixing issues in the VimbisoPay Terminal simulator, specifically in the files:
- `/workspaces/vimbiso-pay/app/core/api/tests/VimbisoPay_Terminal.py`
- `/workspaces/vimbiso-pay/app/core/api/api_interactions.py`


2. Error Handling:
   - The script is not gracefully handling API errors, leading to unhandled exceptions.

3. Missing Attribute:
   - AttributeError: 'CredexBotService' object has no attribute 'utils'.

5. Authentication:
   - There are authentication issues that require updating the environment variables.

## Next Steps
1. After environment refresh:
   - Verify that the new environment variables are set correctly.
   - Re-run the VimbisoPay Terminal simulator to check if the authentication issues are resolved.

2. If authentication is resolved, focus on:
   - Improving error handling in the `refresh_member_info` and `_process_api_response` methods in `api_interactions.py`.
   - Adding the missing 'utils' attribute to the CredexBotService class or removing references to it.
   - Implementing proper message routing and handling for specific user inputs in `VimbisoPay_Terminal.py`.
