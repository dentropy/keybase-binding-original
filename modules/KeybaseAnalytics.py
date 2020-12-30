from database import DB, Messages
from sqlalchemy import func, asc, distinct
import pandas as pd
from datetime import *
from urlextract import URLExtract
from tld import get_fld
import json
import pprint
class KeybaseAnalytics():
    def __init__(self, db_url):
        """KeybaseAnalytics class constructor."""
        self.db = DB(db_url)

    def get_message(self, message_id):
        """Returns a single row from Message object (SQL table) by ID."""
        return self.db.session.query(Messages).get(message_id)

    def get_all_team_messages(self, team):
        """Get all messages from a single team."""
        return self.db.session.query(Messages)\
            .order_by(asc(Messages.sent_time))\
            .filter(Messages.msg_type == "text")\
            .filter(Messages.team == team)

    def get_all_user_messages(self, user):
        """Get all messages from a single user."""
        return self.db.session.query(Messages)\
            .order_by(asc(Messages.sent_time))\
            .filter(Messages.txt_body != None)\
            .filter(Messages.msg_type == "text")\
            .filter(Messages.from_user == user)

    def get_all_topic_messages(self, team, topic):
        """Get all messages from single topic from a specific team."""
        return self.db.session.query(Messages)\
            .order_by(asc(Messages.sent_time))\
            .filter(Messages.txt_body != None)\
            .filter(Messages.msg_type == "text")\
            .filter(Messages.team == team)\
            .filter(Messages.from_user == topic)

    def get_user_messages_from_team(self, team_name, username):
        """Get all messages from a single user on a single team."""
        return self.db.session.query(Messages)\
            .order_by(asc(Messages.sent_time))\
            .filter(Messages.txt_body != None)\
            .filter(Messages.msg_type == "text")\
            .filter(Messages.team == team_name)\
            .filter(Messages.from_user == user)

    def get_num_messages_from_user(self, username):
        """Return object with number of times a text was edited or deleted for a given user."""
        return_object = {}
        return_object["text"] = self.db.session.query(Messages).\
            filter(Messages.from_user == username).\
            filter(Messages.msg_type == "text").count()
        return_object["edit"] = self.db.session.query(Messages).\
            filter(Messages.from_user == username).\
            filter(Messages.msg_type == "edit").count()
        return_object["delete"] = self.db.session.query(Messages).\
            filter(Messages.from_user == username).\
            filter(Messages.msg_type == "delete").count()
        return return_object
    
    def get_num_messages_from_topic(self, topic):
        """Return object with number of times a text was edited or deleted for a given topic."""
        return_object = {}
        return_object["text"] = self.db.session.query(Messages).\
            filter(Messages.topic == topic).\
            filter(Messages.msg_type == "text").count()
        return_object["edit"] = self.db.session.query(Messages).\
            filter(Messages.topic == topic).\
            filter(Messages.msg_type == "edit").count()
        return_object["delete"] = self.db.session.query(Messages).\
            filter(Messages.topic == topic).\
            filter(Messages.msg_type == "delete").count()
        return return_object
    
    def get_list_all_users(self):
        """Update and return list of all users."""
        individual_users = self.db.session.query(distinct(Messages.from_user))
        user_list = []
        for user in individual_users:
            user_list.append(user[0])
        return user_list

    def get_list_all_topics(self):
        """Update and return list of all topics."""
        individual_topic = self.db.session.query(distinct(Messages.topic))
        topic_list = []
        for topic in individual_topic:
            topic_list.append(topic[0])
        return topic_list