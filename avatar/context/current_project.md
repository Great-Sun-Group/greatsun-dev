# Current Project

Finish setting up the greatsun-dev environment while releasing production ready mvps of credex-core and vimbiso-pay by 4am Atlantic time on Monday, in 25 hours.

## Overview
The greatsun-dev environment is designed to facilitate rapid testing and deployment of credex-core and credex-bot. This setup aims to streamline the development and deployment of these services.

## Current State
Greatsun-dev is running but not fully complete, and the clients are well built and tested, but have not yet connected together over the api since significant security upgrades.

## Operational Pipeline

- Finish the core functionality of the greatsun-dev avatar by fixing the terminal bug and implementing: `engage`, `deploy stage`, `deploy prod`.
- Hands-on confirmation that credex-core api is secure and responding to authorized calls.
- Hands-on confirmation that vimbiso-pay is working as expected and processing reponses from the API appropriately.
#### up to here required by 4am Atlantic

- Finish the core functionality of the greatsun-dev avatar with: `stepback`
- Auto-deploy for prod in the DCO.
- Unit tests, integration tests, security tests
- Extended transaction modeling and performance tests.
- Web portal for customer service agents.
- System dashboard to monitor activity and process alerts.
- Initial data visualization and analytics.
- Build out CI/CD pipeline
- Add an avatar-generated summary of every merge to project and merge to dev based on the diff.


# Current Task

Fix the terminal bug: LLM's responses are getting registered by the script as something it should send back to the LLM, creating an endless loop.

## Coming Next
- Deploy to stage
- Deploy to prod (manual, not cron)
- Test in dev and deploy updates

# But First Must Do
Get a 30 minute guided tour of greatsun-dev and the credex-ecosystem software.