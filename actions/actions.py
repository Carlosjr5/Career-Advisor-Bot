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
    
class ActionShowFreQ(Action):

    def name(self) -> Text:
        return "action_show_freQ"

    def parse_question_number(self, text: Text) -> int:
        # Logic to extract question number from user input
        if "first" in text:
            return 1
        elif "second" in text:
            return 2
        elif "third" in text:
            return 3
        elif "fourth" in text:
            return 4
        elif "no5" in text:
            return 5
        elif "no6" in text:
            return 6
        elif "no7" in text:
            return 7
        elif "no8" in text:
            return 8
        elif "no9" in text:
            return 9
        elif "no10" in text:
            return 10
        elif "no11" in text:
            return 11
        elif "no12" in text:
            return 12
        else:
            return 0  

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topics = topic_api.fetch_topics()
        results = topic_api.format_topics(topics)
        readable = topic_api.format_topics(topics['freQ'], header=False)

        # Parse user's request for a specific question number
        user_input = tracker.latest_message.get("text", "")
        question_number = self.parse_question_number(user_input)

        # Clarify which question the user is referring to
        
        if question_number == 1:
            dispatcher.utter_message(text="Do you want to learn more about data analysis?")
        elif question_number == 2:
            dispatcher.utter_message(text="Do you want to know more about a career in cybersecurity?")
        elif question_number == 3:
            dispatcher.utter_message(text="Do you mean you want to know about a career in software engineering?")
        elif question_number == 4:
            dispatcher.utter_message(text="Do you want to learn about cloud computing careers?")
        elif question_number == 5:
            dispatcher.utter_message(text="Are you exploring career options in artificial intelligence?")
        elif question_number == 6:
            dispatcher.utter_message(text="Are you interested in specializing in database administration?")
        elif question_number == 7:
            dispatcher.utter_message(text="Are you looking to become a UX/UI designer?")
        elif question_number == 8:
            dispatcher.utter_message(text="Are you interested in the career prospects for data engineering?")
        elif question_number == 9:
            dispatcher.utter_message(text="Are you curious about the career paths available in mobile app development?")
        elif question_number == 10:
            dispatcher.utter_message(text="Are you considering transitioning from software engineering to product management?")
        elif question_number == 11:
            dispatcher.utter_message(text="Are you interested in learning about opportunities in IT project management?")
        elif question_number == 12:
            dispatcher.utter_message(text="Do you want to know how to become a data scientist?")
        else:
            dispatcher.utter_message(text=f"Here are some frequently asked questions by the users:\n\n{readable}")
            return [SlotSet("results", results)]

        return []

      


topic_api = TopicAPI()
chatGPT = ChatGPT()
