import json
import random

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionRetrieveFact(Action):

    def name(self) -> Text:
        return "action_retrieve_fact"

    def __retrieve_fact(self, key: Text) -> Text:
        """returns fact according to key or empty string on failing"""
        
        with open('fake_db.json') as db:
            db_data: Dict = json.load(db)
        
        values = db_data.get(key, [])
        
        if len(values):
            return random.choice(values)
        else:
            return ''

    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]
    ]:
        topic = tracker.get_slot('topic')
        fact = self.__retrieve_fact(topic)

        if fact == '':
            dispatcher.utter_message(text="I could not find anything about {topic} :(")
        else:
            dispatcher.utter_message(text="I've found something interesting for you:")
            dispatcher.utter_message(text=fact)

        return [SlotSet(key='topic', value=None)]