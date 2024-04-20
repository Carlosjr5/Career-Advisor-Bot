from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGPT3Fallback(Action):
    def name(self) -> Text:
        return "action_gpt3_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_input = tracker.latest_message.get('text')
        openai.api_key = "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"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        gpt3_response = response.choices[0].text.strip()
        dispatcher.utter_message(text=gpt3_response)
        return []