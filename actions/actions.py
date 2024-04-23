import os
from typing import Any, Text, Dict, List
import pandas as pd
import requests
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.events import SlotSet
import openai
import json


class TopicAPI:
    def __init__(self):
        # Load topics from a CSV file
        self.db = pd.read_csv("topics.csv")

    def fetch_topics(self):
        return self.db

    def format_topics(self, df, header=True) -> str:
        return df.to_csv(index=False, header=header)


class ChatGPT(object):

    def __init__(self):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('sk-proj-')}"
        }
        self.prompt = "Answer the following question, based on the data shown. " \
                      "Answer in a complete sentence and don't say anything else."

    def ask(self, topics, question):
        content = self.prompt + "\n\n" + topics + "\n\n" + question
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": content}]
        }
        result = requests.post(
            url=self.url,
            headers=self.headers,
            json=body,
        )
        return result.json()["choices"][0]["message"]["content"]


class ActionShowTopics(Action):

    def name(self) -> Text:
        return "action_show_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topics = topic_api.fetch_topics()
        results = topic_api.format_topics(topics)
        readable = topic_api.format_topics(topics['topics'], header=False)
        dispatcher.utter_message(
            text=f"Here are some topics you can find when studying computer science:\n\n{readable} Which one interest you the most?:")
        return [SlotSet("results", results)]


class ActionShowTopicInfo(Action):

    def name(self) -> Text:
        return "action_show_topic_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Fetch the user's chosen topic from the slot
        chosen_topic = tracker.get_slot('topic')
        if not chosen_topic:
            dispatcher.utter_message(text="Please specify a topic you are interested in.")
            return []

        # Fetch topics
        topics = topic_api.fetch_topics()
        # Filter the DataFrame to find the matching topic's information
        topic_info = topics[topics['topics'].str.lower() == chosen_topic.lower()]

        # Prepare the message text
        if not topic_info.empty:
            information = topic_info.iloc[0]['information']
            message_text = f"Here is information about the '{chosen_topic}' topic:\n\n{information}"
        else:
            message_text = f"No information available for the topic '{chosen_topic}'."

        # Dispatch the message
        dispatcher.utter_message(text=message_text)

        return []



class ActionShowFreQ(Action):

    def name(self) -> Text:
        return "action_show_freQ"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topics = topic_api.fetch_topics()
        results = topic_api.format_topics(topics)
        readable = topic_api.format_topics(topics['freQ'], header=False)
        dispatcher.utter_message(text=f"Here are some frequently questions by the users :\n\n{readable}")

        return [SlotSet("results", results)]




topic_api = TopicAPI()
chatGPT = ChatGPT()
