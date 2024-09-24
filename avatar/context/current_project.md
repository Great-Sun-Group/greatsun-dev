# Current Project

## End State
Production-ready mvps of credex-core and vimbiso-pay are realeased.

## Current State
Greatsun-dev container mostly operational, avatar script still buggy. Submodule servers confirmed running on local ports, but not tested.

## Next Steps Planned

Test all main member action flows with simulation scripts.

- First finish core avatar functions and suppress and conversationalize terminal messages except errors on:
    - `avatar engage`
    - `avatar load`
    - `avatar commit`
    - `avatar submit`


- Move simulation scripts from vimbiso-pay to greatsun-dev

- Test WhatsApp Simulation Interface
   - Thoroughly test the `simulate_user.py` script to ensure it accurately simulates WhatsApp interactions.
   - Verify that all types of messages (text, interactive, etc.) are handled correctly.
   - Test error handling and edge cases in the simulation.

- Enhance Interactive Message Handling
   - Implement proper display and handling of interactive messages (e.g., buttons, list options).
   - Ensure that user responses to interactive messages are correctly processed.

- Currently experiencing issues in the VimbisoPay Terminal simulator, specifically in the files:
   - `/workspaces/vimbiso-pay/app/core/api/tests/VimbisoPay_Terminal.py`
   - `/workspaces/vimbiso-pay/app/core/api/api_interactions.py`
   - Error Handling:
      - The script is not gracefully handling API errors, leading to unhandled exceptions.
   - Missing Attribute:
      - AttributeError: 'CredexBotService' object has no attribute 'utils'.
   - To focus on:
      - Improving error handling in the `refresh_member_info` and `_process_api_response` methods in `api_interactions.py`.
      - Adding the missing 'utils' attribute to the CredexBotService class or removing references to it.
      - Implementing proper message routing and handling for specific user inputs in `VimbisoPay_Terminal.py`.
