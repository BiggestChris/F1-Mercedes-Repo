from flask import Flask, render_template, request, url_for, redirect
from openai import OpenAI
import re, os
from dotenv import load_dotenv # Add
import csv

load_dotenv() # Add

client = OpenAI()

app = Flask(__name__)


'''
Pseudo-code for final solution
1. Pull in the API for Radio Comms from Open F1 (during a live race would need to pull in from a radio channel directly)
    a. GET https://api.openf1.org/v1/team_radio
2. Save down audio comms links to a database
3. Run audio comms through Google Cloud Speech-to-Text API (https://cloud.google.com/speech-to-text?hl=en)
4. Then run written radio comms through ChatGPT
    a. Apply a wrapper to look for below keywords as indicating a change in strategy:
        {
        plan,
        thinking,
        strategy,
        use,
        }
    b. Apply a wrapper to look for below words with numbers indicating an upcoming change:
        {
        plus
        }
5. Pull written radio comms into a live chat-feed on a webpage (may need JavaScript to dynamically update)
6. Have output from ChatGPT when it finds the above to give an alert - along with a translation to information and action to take
'''


@app.route("/")
def index():
    messages = []

    # TODO: Link to OpenF1 API directly to pull in radio transmissions
    # TODO: Link to transcription API to translate audio files to text
    # Read the CSV file and extract quotes/messages
    with open('Radio_records.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row['Quote'] != 'BLANK':  # Ignore BLANK quotes
                messages.append(row['Quote'])

    # TODO: Refactor so ChatGPT isn't being called every time the application is run, but every time a new message is fed in
    completions = []
    for message in messages:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # TODO: Link to an SQL database, to pull relevant content and store learnings on how to best apply AI wrapper
            messages=[
                 {"role": "system", 
                  "content": """You are processing radio communications of an F1 race.
                  Please print out the radio communication as it is at first, preface it with 'comms:' then in a sentence summarise the information that conveys, preface that with 'info:'.
                  If you see any of the words 'plan, thinking, use, do not use' then that means there is a change in strategy, if you see that please tell the user to be on alert for it.
                  If you see any mention of 'plus or +' and a number (N), it likely means a change in strategy in N laps, so please convey that. For both of those please preface with 'ADVICE:'
                  To summarise the outputs should be in the form of 'comms: (exact copy of message) [new line], info: (single sentence summary of info) [new line], ADVICE: (action to take - this will not exist for most lines, if there's no advice or advice is 'None' PLEASE don't populate or create this line)
                  """},
                {"role": "user",
                 "content": message }
            ]
        )

        # Extract comms, info, and advice from the completion
        comms = message
        info = "" # Initialise info as empty string
        advice = ""  # Initialise advice as empty string

        message_content = completion.choices[0].message.content
        words = message_content.split()  # Split the string into words

        try:
            # Find the index where 'info:' occurs and start on the next word
            start_index = words.index('info:') + 1
            # Iterate through the words starting from 'info:' until 'ADVICE:' is found or the end of the string
            for word in words[start_index:]:
                if word == "ADVICE:":
                    # If 'ADVICE:' is found, break the loop
                    break
                info += word + " "  # Append the word to the info string along with a space
        except ValueError:
            # Handle cases where 'info:' is not found
            pass

        # Find the index where 'ADVICE:' occurs and start on the next word
        try:
            advice_index = words.index('ADVICE:') + 1
            for word in words[advice_index:]:
                advice += word + " "  # Append the word to the advice string along with a space
        except ValueError:
            # Handle cases where 'ADVICE:' is not found
            pass

        # Store comms, info, and advice in a dictionary
        completion_data = {
            "comms": comms,
            "info": info,
            "advice": advice
        }

        print(completion_data)

        completions.append(completion_data)
    
    last_completion_with_advice = {}

    # Iterate over completions in reverse order to get latest alert
    for completion in reversed(completions):
        # Check if the completion contains advice
        if completion.get('advice') is not None and completion.get('advice').strip() != 'None' and completion.get('advice') != '':
            last_completion_with_advice = completion
            break  # Exit the loop once the last completion with advice is found

    return render_template("index.html", completions=completions, last_completion_with_advice=last_completion_with_advice)