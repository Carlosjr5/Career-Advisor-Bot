import os
from typing import Any, Text, Dict, List
import pandas as pd
import requests
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.events import SlotSet
import re

class TopicAPI:
    def __init__(self):
        # Load topics from a CSV file
        self.db = pd.read_csv("topics.csv")

    def fetch_topics(self):
        return self.db

    def format_topics(self, df, header=True) -> str:
        return df.to_csv(index=False, header=header)



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
            text=f"Here are some topics you can find when studying computer science:\n\n{readable}")
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
        # Create a regex pattern to match variations like 'mobile apps' -> 'mobile app'
        pattern = re.compile(r'\b' + re.escape(chosen_topic) + r's?\b', re.IGNORECASE)

        # Filter the DataFrame to find the matching topic's information using regex
        match = topics['topics'].apply(lambda x: bool(pattern.search(x)))
        matched_topics = topics[match]

        # Prepare the message text
        if not matched_topics.empty:
            information = "; ".join(matched_topics['information'].tolist())
            message_text = f"Here is information about topics related to '{chosen_topic}':\n\n{information}"
        else:
            message_text = f"No information available for topics related to '{chosen_topic}'."

        # Dispatch the message
        dispatcher.utter_message(text=message_text)

        return []

class ActionShowTopicLO(Action):
    def name(self) -> Text:
        return "action_show_topic_lo"

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
        # Filter the DataFrame to find the matching topic's information using a case-insensitive substring match
        topic_info = topics[topics['topics'].str.lower().str.contains(chosen_topic.lower(), na=False)]

        # Prepare the message text
        if not topic_info.empty:
            information = "; ".join(topic_info['learning_outcome'].tolist())
            message_text = f"Here are the learning outcomes :\n\n{information}"
        else:
            message_text = f"No information available for topics related to '{chosen_topic}'."

        # Dispatch the message
        dispatcher.utter_message(text=message_text)

        return []


class ActionShowTopicCareerFuture(Action):
    def name(self) -> Text:
        return "action_show_topic_career_future"

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
        # Filter the DataFrame to find the matching topic's information using a case-insensitive substring match
        topic_info = topics[topics['topics'].str.lower().str.contains(chosen_topic.lower(), na=False)]

        # Prepare the message text
        if not topic_info.empty:
            information = "; ".join(topic_info['career_future'].tolist())
            message_text = f"Here are the career opportunities :\n\n{information}"
        else:
            message_text = f"No information available for topics related to '{chosen_topic}'."

        # Dispatch the message
        dispatcher.utter_message(text=message_text)

        return []


class ActionShowTopicDegree(Action):
    def name(self) -> Text:
        return "action_show_topic_degree"

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
        # Filter the DataFrame to find the matching topic's information using a case-insensitive substring match
        topic_info = topics[topics['topics'].str.lower().str.contains(chosen_topic.lower(), na=False)]

        # Prepare the message text
        if not topic_info.empty:
            information = "; ".join(topic_info['degree'].tolist())
            message_text = f"\n\n{information}"
        else:
            message_text = f"No information available for topics related to '{chosen_topic}'."

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
        dispatcher.utter_message(text=f"Sorry, I can´t help solving your query.\n\nHere are some frequently questions by other students :\n\n{readable}")

        return [SlotSet("results", results)]




class ActionShowTopicComparison(Action):
    def name(self) -> Text:
        return "action_show_topic_comparison"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Assuming topics can be extracted from entities
        topics = [entity.get('value') for entity in tracker.latest_message['entities'] if
                  entity.get('entity') == 'topic']

        if len(topics) < 2:
            dispatcher.utter_message(text="Please specify at least two topics to compare.")
            return []

        # Fetch all topics from the dataset
        dataset = topic_api.fetch_topics()

        comparisons = []
        for topic in topics:
            topic_data = dataset[dataset['topics'].str.lower().str.contains(topic.lower(), na=False)]
            if not topic_data.empty:
                learning_outcomes = "; ".join(topic_data['learning_outcome'].tolist())
                career_futures = "; ".join(topic_data['career_future'].tolist())
                comparisons.append(
                    f"**{topic.capitalize()}**:\nLearning Outcomes: \n\n{learning_outcomes}\nCareer Opportunities: \n\n{career_futures}\n")
            else:
                comparisons.append(f"No data available for '{topic}'.")

        # Prepare the comparison message
        comparison_message = "\n\n".join(comparisons)
        message_text = f"Comparing topics:\n\n{comparison_message}"

        # Dispatch the message
        dispatcher.utter_message(text=message_text)

        return []


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



topic_api = TopicAPI()
chatGPT = ChatGPT()
