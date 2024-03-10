Credit:
    This project has been built with Python and Flask - numerous code parts has been taken from another one of my apps that I have built - CS50 Final Project.


Following documentation has been added to the repo in PDF format for further explanation of problem/solution:
    1 Comprehensive Problem Statement
    2 Solution architecture
    3 Figma Mock-up
    4 MVP architecture


Quantative research carried out can be viewed at this URL: https://docs.google.com/spreadsheets/d/1PPFe2oYYzyMScTtS1BzCpKjAhZN9DOcwOAxkHEuqj0g/edit?usp=sharing


MVP Details:
    For an MVP - this is a relatively static Flask app that calls ChatGPT API when it is run on the static data currently stored in a CSV. This is to test that ChatGPT could interpret data for actionable information.

    The loading up of the application also takes a significant amount of time, when F1 races would not have that luxury, so this would need to be improved upon.

    In the final solution, I would want to feed in radio communications directly, and update in real-time, alongside ChatGPT API running in real-time.

    API Key for ChatGPT is documented in a .env which is gitignore'd


AI Notes:
    ChatGPT may not been the long-term solution (due to cost and time to run), also it does function partly like a black-box inside the API itself which would cause problems. There may be other AI solutions that would work better long-term.

    Because the API is being called every time Flask is run, there may be different responses from ChatGPT each time.