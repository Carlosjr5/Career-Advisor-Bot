# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai

class GPT3Action(Action):
    def name(self) -> Text:
        return "action_gpt3_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_input = tracker.latest_message.get('text')

     
        openai.api_key = ""  #api key

       
        response = openai.Completion.create(
            engine="text-davinci-003",  # eingine
            prompt=user_input,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        #  generated response from the API
        gpt3_response = response.choices[0].text.strip()

        # Send the response back to the user
        dispatcher.utter_message(text=gpt3_response)

        return []