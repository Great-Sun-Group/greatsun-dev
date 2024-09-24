# Current Project

## End State
Production-ready mvps of credex-core and vimbiso-pay are realeased.

## Current State
Greatsun-dev container mostly operational, avatar script still buggy. Submodule servers confirmed running on local ports, but not tested.

## Next Steps Planned

Test all main member action flows with simulation scripts.

- Move simulation scripts from vimbiso-pay to greatsun-dev

- Test WhatsApp Simulation Interface
   - Thoroughly test the `simulate_user.py` script to ensure it accurately simulates WhatsApp interactions.
   - Verify that all types of messages (text, interactive, etc.) are handled correctly.
   - Test error handling and edge cases in the simulation.

- Enhance Interactive Message Handling
   - Implement proper display and handling of interactive messages (e.g., buttons, list options).
   - Ensure that user responses to interactive messages are correctly processed.

- Fix issues in the VimbisoPay Terminal simulator:
   - Improve error handling in the `refresh_member_info` and `_process_api_response` methods in `api_interactions.py`.
   - Add the missing 'utils' attribute to the CredexBotService class or remove references to it.
   - Implement proper message routing and handling for specific user inputs in `VimbisoPay_Terminal.py`.

- Set up Development Environment:
   - Ensure that the `vimbiso-pay` and `credex-core` submodules are properly set up and running in dev mode.
   - Configure the `VIMBISO_PAY_API_URL` constant in `api_interactions.py` to point to the correct local development server URL.

- Testing:
   - Write unit tests for the `APIInteractions` class to ensure that the API interactions are working correctly.
   - Test the `vimbisopay_terminal.py` script by running it and simulating different user inputs and actions.
   - Verify that the script is able to communicate with the `vimbiso-pay` submodule and retrieve the expected data from the `credex-core` submodule.