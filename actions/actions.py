from typing import Any, Text, Dict, List
import pandas as pd
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


def unify_topic_name(topic: Text) -> Text:
    synonym_map = {
        "ai": "artificial intelligence",
        "artificial intel": "artificial intelligence",
        "a.i.": "artificial intelligence",
        "intelligent systems": "artificial intelligence",
        "ml": "artificial intelligence",
        "mach learning": "artificial intelligence",
        "machine learn": "artificial intelligence",

        "cyber": "cybersecurity",
        "info security": "cybersecurity",
        "cyber-sec": "cybersecurity",
        "cyber sec": "cybersecurity",
        "security tech": "cybersecurity",

        "data analysis": "data analysis",
        "data analytics": "data analysis",
        "analytics": "data scientist",
        "analyzing data": "data scientist",
        "data analys": "data scientist",

        "software dev": "software engineering",
        "soft eng": "software engineering",
        "soft development": "software engineering",
        "program development": "software engineering",

        "cloud tech": "cloud computing",
        "cloud comp": "cloud computing",
        "cloud-based tech": "cloud computing",
        "online computing": "cloud computing",

        "db": "database",
        "database systems": "database",
        "data bases": "database",
        "db systems": "database",

        "ui": "ui design",
        "user interface design": "ui design",
        "ux design": "ui design",
        "ux/ui design": "ui design",
        "user experience design": "ui design",

        "data eng": "data engineering",
        "data engineering tech": "data engineering",
        "data engineer tech": "data engineering",

        "app development": "mobile app development",
        "mobile app dev": "mobile app development",
        "app dev": "mobile app development",
        "smartphone app development": "mobile app development",

        "product mgmt": "product management",
        "product management tech": "product management",
        "prod mgmt": "product management",
        "product admin": "product management",

        "it mgmt": "IT management",
        "it management tech": "IT management",
        "information tech management": "IT management",
        "technology management": "IT management",

        "data scientist": "data scientist",
        "data science expert": "data scientist",
        "data professional": "data scientist",
       
    }
    return synonym_map.get(topic.lower(), topic)


class ActionShowTopics(Action):

    def name(self) -> Text:
        return "action_show_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topics = topic_api.fetch_topics()
        if 'all' in topics.columns and not topics['all'].empty:
            first_topic = topics['all'].iloc[0]
            dispatcher.utter_message(
                text=f"Here's a topic you can find when studying computer science:\n\n{first_topic}\n\nWould you like to learn more about this topic?")
        else:
            dispatcher.utter_message(text="Sorry, no topics are available at the moment.")

        return []


class ActionShowTopicInfo(Action):
    def name(self) -> Text:
        return "action_show_topic_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_topic = tracker.get_slot('topic')
        if not chosen_topic:
            dispatcher.utter_message(text="I'm not sure which topic you're interested in. Could you specify?")
            return []

        # Normalize the topic name using the synonym map
        unified_topic = unify_topic_name(chosen_topic)

        topics = topic_api.fetch_topics()
        pattern = re.compile(r'\b' + re.escape(unified_topic) + r's?\b', re.IGNORECASE)
        match = topics['topics'].apply(lambda x: bool(pattern.search(x)))
        matched_topics = topics[match]

        if not matched_topics.empty:
            information = "; ".join(matched_topics['information'].tolist())
            dispatcher.utter_message(
                text=f"Information about {unified_topic}:\n\n{information}\n\nLet me know if you want to know more about the learning outcomes or career future in this field!")
        else:
            dispatcher.utter_message(text=f"I couldn't find information related to '{unified_topic}'.")

        return []


class ActionShowTopicLO(Action):
    def name(self) -> Text:
        return "action_show_topic_lo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_topic = tracker.get_slot('topic')
        if not chosen_topic:
            dispatcher.utter_message(text="Please specify a topic you are interested in.")
            return []

        # Normalize the topic name using the synonym map
        unified_topic = unify_topic_name(chosen_topic)

        # Fetch topics
        topics = topic_api.fetch_topics()
        # Filter the DataFrame to find the matching topic's information using a case-insensitive substring match
        topic_info = topics[topics['topics'].str.lower().str.contains(unified_topic.lower(), na=False)]

        # Prepare the message text
        if not topic_info.empty:
            information = "; ".join(topic_info['learning_outcome'].tolist())
            message_text = f"Here are the learning outcomes for {unified_topic}:\n\n{information}"
        else:
            message_text = f"No information available for topics related to '{unified_topic}', could you clarify the topic you are interested in?."

        # Dispatch the message
        dispatcher.utter_message(text=message_text)

        return []


class ActionShowTopicCareerFuture(Action):
    def name(self) -> Text:
        return "action_show_topic_career_future"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_topic = tracker.get_slot('topic')
        if not chosen_topic:
            dispatcher.utter_message(text="Please specify a topic you are interested in.")
            return []

        # Normalize the topic name using the synonym map
        unified_topic = unify_topic_name(chosen_topic)

        # Fetch topics
        topics = topic_api.fetch_topics()
        # Filter the DataFrame to find the matching topic's information using a case-insensitive substring match
        topic_info = topics[topics['topics'].str.lower().str.contains(unified_topic.lower(), na=False)]

        # Prepare the message text
        if not topic_info.empty:
            information = "; ".join(topic_info['career_future'].tolist())
            message_text = f"Here are the career opportunities in {unified_topic}:\n\n{information}"
        else:
            message_text = f"No information available for topics related to '{unified_topic}', could you clarify the topic you are interested in?."

        # Dispatch the message
        dispatcher.utter_message(text=message_text)

        return []


class ActionShowTopicDegree(Action):
    def name(self) -> Text:
        return "action_show_topic_degree"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_topic = tracker.get_slot('topic')
        if not chosen_topic:
            dispatcher.utter_message(text="Please specify a topic you are interested in.")
            return []

        # Normalize the topic name using the synonym map
        unified_topic = unify_topic_name(chosen_topic)

        # Fetch topics
        topics = topic_api.fetch_topics()
        # Filter the DataFrame to find the matching topic's information using a case-insensitive substring match
        topic_info = topics[topics['topics'].str.lower().str.contains(unified_topic.lower(), na=False)]

        # Prepare the message text
        if not topic_info.empty:
            information = "; ".join(topic_info['degree'].tolist())
            message_text = f"Here are the degree options available for {unified_topic}:\n\n{information}"
        else:
            message_text = f"No degree information available for topics related to '{unified_topic}'."

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
        if 'questions' in topics.columns and not topics['questions'].empty:
            first_question = topics['questions'].iloc[0]
            dispatcher.utter_message(text=f"Sorry, I can't help solve your query directly. Here's a frequently asked question by other students:\n\n{first_question}")
        else:
            dispatcher.utter_message(text="Sorry, no frequently asked questions are available at the moment.")

        return []


class ActionShowTopicComparison(Action):
    def name(self) -> Text:
        return "action_show_topic_comparison"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract topics from entities, applying synonym normalization
        topics = [unify_topic_name(entity.get('value')) for entity in tracker.latest_message['entities'] if
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
                information = "; ".join(topic_data['information'].tolist())
                learning_outcomes = "; ".join(topic_data['learning_outcome'].tolist())
                career_futures = "; ".join(topic_data['career_future'].tolist())
                comparisons.append(
                    f"**{topic.capitalize()}**:\n {information} \n Learning Outcomes: \n\n{learning_outcomes}\nCareer Opportunities: \n\n{career_futures}\n")
            else:
                comparisons.append(f"No data available for '{topic}'.")

        # Prepare the comparison message
        comparison_message = "\n\n".join(comparisons)
        message_text = f"Comparing topics:\n\n{comparison_message}"

        # Dispatch the message
        dispatcher.utter_message(text=message_text)

        return []


class ActionClarifyTopic(Action):
    def name(self) -> Text:
        return "action_clarify_topic"

    def parse_question_number(self, text: Text) -> int:
        mapping = {
            "first": 1, "second": 2, "third": 3, "fourth": 4,
            "5": 5, "6": 6, "7": 7, "8": 8,
            "9": 9, "10": 10, "11": 11, "12": 12
        }
        for key, value in mapping.items():
            if key in text:
                return value
        return 0

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        topics = topic_api.fetch_topics()
        results = topic_api.format_topics(topics)
        readable = topic_api.format_topics(topics['freQ'], header=False)

        user_input = tracker.latest_message.get("text", "")
        question_number = self.parse_question_number(user_input)

        topic_prompts = [
            "data analysis", "cybersecurity", "software engineering",
            "cloud computing", "artificial intelligence", "database administration",
            "UX/UI design", "data engineering", "mobile app development",
            "product management", "IT project management", "data scientist"
        ]

        # Normalize the topic names in the list to use canonical names
        normalized_topics = [unify_topic_name(topic) for topic in topic_prompts]

        # Set the topic slot based on question number and ask for confirmation
        if 1 <= question_number <= len(normalized_topics):
            topic = normalized_topics[question_number - 1]
            dispatcher.utter_message(text=f"Do you want to learn more about {topic}?")
            return [SlotSet("topic", topic)]
        else:
            first_question = topics['questions'].iloc[0]
            dispatcher.utter_message(text=f"Sorry, I can't help solve your query directly. Here's a frequently asked question by other students:\n\n{first_question}")
            return [SlotSet("results",results)]
       


topic_api = TopicAPI()
