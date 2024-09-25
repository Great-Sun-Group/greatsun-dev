# Current Project

## End State
Production-ready mvps of credex-core and vimbiso-pay are realeased.

## Current State
Greatsun-dev container operational, avatar script online. Submodule servers confirmed running on local ports, testing in progress.

## Next Steps Planned

Test all main member action flows with simulation scripts.

- WhatsApp Simulation Interface
   - Verify that all types of messages (text, interactive, etc.) are handled correctly.
   - Implement proper display and handling of interactive messages (e.g., buttons, list options).
   - Ensure that user responses to interactive messages are correctly processed.
   - Test the `vimbisopay_terminal.py` script by running it and simulating different user inputs and actions.
   - Verify that the script is able to communicate with the `vimbiso-pay` submodule and retrieve the expected data from the `credex-core` submodule.

- Fix issues in the VimbisoPay Terminal simulator:
   - Improve error handling in the `refresh_member_info` and `_process_api_response` methods in `api_interactions.py`.
   - Add the missing 'utils' attribute to the CredexBotService class or remove references to it.
   - Implement proper message routing and handling for specific user inputs in `VimbisoPay_Terminal.py`.

- Testing:
   - Write unit tests for the `APIInteractions` class to ensure that the API interactions are working correctly.
