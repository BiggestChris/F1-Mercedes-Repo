This project has been built with Flask, numerous code has been taken from another one of my apps that I have built - CS50 Final Project.

For an MVP - this is a relatively static Flask app that calls ChatGPT API when it is run on the static data currently stored in a CSV. This is to test that ChatGPT could interpret data for actionable information.

In practice, I would want to feed in radio communications directly, and update in real-time, alongside ChatGPT API running in real-time.

ChatGPT may nto been the long-term solution (due to cost and time to run), also it does function partly like a black-box inside the API itself which would cause problems. There may be other AI solutions that would work better long-term.

Because the API is being called every time Flask is run, there may be different responses from ChatGPT each time.

API Key for ChatGPT is documented in a .env which is gitignore'd


Notes:
Following documentation has been added to the repo in PDF format
Comprehensive Problem Statement
Solution architecture
Figma Mock-up
MVP architecture
