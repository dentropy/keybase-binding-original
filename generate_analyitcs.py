'''
GeneratedAnalyitcs Object
GeneratedAnalyitcs.user_list
GeneratedAnalyitcs.topic_list
GeneratedAnalyitcs.characters_per_user
GeneratedAnalyitcs.characters_per_topic
GeneratedAnalyitcs.messages_per_user
GeneratedAnalyitcs.messages_per_topic
GeneratedAnalyitcs.num_users_per_topic
'''
from database import DB, Messages
from sqlalchemy import func
from sqlalchemy import distinct

class GeneratedAnalyitcs():
    def __init__(self, db_url):
        self.db = DB(db_url)
        self.get_list_all_users()
        self.get_list_all_topics()
        self.get_characters_per_user()
        self.get_characters_per_topic()
        self.get_messages_per_user()
        self.get_messages_per_topic()
        self.get_number_users_per_topic()
        
    def get_list_all_users(self):
        individual_users = self.db.session.query(distinct(Messages.from_user))
        self.user_list = []
        for user in individual_users:
            self.user_list.append(user[0])
        return self.user_list

    def get_list_all_topics(self):
        individual_topic = self.db.session.query(distinct(Messages.topic))
        self.topic_list = []
        for topic in individual_topic:
            self.topic_list.append(topic[0])
        return self.topic_list

    def get_characters_per_user(self):
        messages_per_user = {}
        for user in self.user_list:
            messages_per_user[user] = 0
            user_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(from_user=user)
            for message in user_messages:
                messages_per_user[user] += len(message.txt_body)
        list_of_users = sorted(messages_per_user, key = messages_per_user.get, reverse=True)
        self.characters_per_user = {"users_list":[], "characters_list":[], "users":{}}
        for item in list_of_users:
            self.characters_per_user["users_list"].append(item)
            self.characters_per_user["characters_list"].append(messages_per_user[item])
            self.characters_per_user["users"][item] = messages_per_user[item]
        return self.characters_per_user

    def get_characters_per_topic(self):
        messages_per_topic = {}
        for topic in self.topic_list:
            messages_per_topic[topic] = 0
            topic_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
            for message in topic_messages:
                messages_per_topic[topic] += len(message.txt_body)
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.characters_per_topic = []
        for item in list_of_users:
            self.characters_per_topic.append([item, messages_per_topic[item]])
        return self.characters_per_topic

    def get_messages_per_user(self):
        messages_per_user = {}
        for user in self.user_list:
            messages_per_user[user] = 0
            user_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(from_user=user)
            messages_per_user[user] = user_messages.count()
        list_of_users = sorted(messages_per_user, key = messages_per_user.get, reverse=True)
        self.messages_per_user = []
        for item in list_of_users:
            self.messages_per_user.append([item, messages_per_user[item]])
        return self.messages_per_user

    def get_messages_per_topic(self):
        messages_per_topic = {}
        for topic in self.topic_list:
            messages_per_topic[topic] = 0
            topic_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
            messages_per_topic[topic] = topic_messages.count()
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.messages_per_topic = []
        for item in list_of_users:
            self.messages_per_topic.append([item, messages_per_topic[item]])
        return self.messages_per_topic

    def get_number_users_per_topic(self):
        messages_per_topic = {}
        for topic in self.topic_list:
            topic_messages = self.db.session.query(distinct(Messages.from_user)).filter(Messages.txt_body != None).filter_by(topic=topic)
            messages_per_topic[topic] = topic_messages.count()
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.num_users_per_topic = []
        for item in list_of_users:
            self.num_users_per_topic.append([item, messages_per_topic[item]])
        return self.num_users_per_topic

'''
GeneratedAnalyitcs Object Definition
GeneratedAnalyitcs.user_list
GeneratedAnalyitcs.topic_list
GeneratedAnalyitcs.characters_per_user
GeneratedAnalyitcs.characters_per_topic
GeneratedAnalyitcs.messages_per_user
GeneratedAnalyitcs.messages_per_topic
GeneratedAnalyitcs.num_users_per_topic
'''

gen_an = GeneratedAnalyitcs("sqlite:///complexityweekend.sqlite")
print(gen_an.characters_per_user)
