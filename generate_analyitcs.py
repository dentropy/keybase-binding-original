from database import DB, Messages
from sqlalchemy import func
from sqlalchemy import distinct

class GeneratedAnalyitcs():
    def __init__(self, db_url):
        self.db = DB(db_url)
        self.get_messages()
        self.get_list_all_users()
        self.get_list_all_topics()
        self.get_characters_per_user()
        self.get_characters_per_topic()
        self.get_messages_per_user()
        self.get_messages_per_topic()
        self.get_number_users_per_topic()
        self.get_reaction_per_message()
        self.get_reaction_sent_per_user()
        self.get_reaction_type_popularity()
        

    def get_messages(self):
        text_messages = self.db.session.query(Messages).filter(Messages.msg_type == "text")
        self.messages = {}
        for message in text_messages:
            self.messages[message.id] = {}
            self.messages[message.id]["team"] = message.team
            self.messages[message.id]["from_user"] = message.from_user
            self.messages[message.id]["topic"] = message.topic
            self.messages[message.id]["txt_body"] = message.txt_body
            
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
        self.characters_per_user = {"users_list":[], "characters_list":[]}
        for item in list_of_users:
            self.characters_per_user["users_list"].append(item)
            self.characters_per_user["characters_list"].append(messages_per_user[item])
        return self.characters_per_user

    def get_characters_per_topic(self):
        messages_per_topic = {}
        for topic in self.topic_list:
            messages_per_topic[topic] = 0
            topic_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
            for message in topic_messages:
                messages_per_topic[topic] += len(message.txt_body)
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.characters_per_topic = {"topics_list":[], "characters_list":[]}
        for item in list_of_users:
            self.characters_per_topic["topics_list"].append(item)
            self.characters_per_topic["characters_list"].append(messages_per_topic[item])
        return self.characters_per_topic

    def get_messages_per_user(self):
        messages_per_user = {}
        for user in self.user_list:
            messages_per_user[user] = 0
            user_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(from_user=user)
            messages_per_user[user] = user_messages.count()
        list_of_users = sorted(messages_per_user, key = messages_per_user.get, reverse=True)
        self.messages_per_user = {"users_list":[], "messages_list":[]}
        for item in list_of_users:
            self.messages_per_user["users_list"].append(item)
            self.messages_per_user["messages_list"].append(messages_per_user[item])
        return self.messages_per_user

    def get_messages_per_topic(self):
        messages_per_topic = {}
        for topic in self.topic_list:
            messages_per_topic[topic] = 0
            topic_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
            messages_per_topic[topic] = topic_messages.count()
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.messages_per_topic = {"topics_list":[], "messages_list":[]}
        for item in list_of_users:
            self.messages_per_topic["topics_list"].append(item)
            self.messages_per_topic["messages_list"].append(messages_per_topic[item])
        return self.messages_per_user

    def get_number_users_per_topic(self):
        messages_per_topic = {}
        for topic in self.topic_list:
            topic_messages = self.db.session.query(distinct(Messages.from_user)).filter(Messages.txt_body != None).filter_by(topic=topic)
            messages_per_topic[topic] = topic_messages.count()
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.number_users_per_topic = {"users_list":[], "topics_list":[]}
        for item in list_of_users:
            self.number_users_per_topic["users_list"].append(item)
            self.number_users_per_topic["topics_list"].append(messages_per_topic[item])
        return self.number_users_per_topic


    def get_reaction_per_message(self):
        messages = {}
        topic_messages = self.db.session.query(Messages).filter(Messages.msg_type == "reaction")
        for message in topic_messages:
            if message.reaction_reference not in messages:
                messages[message.reaction_reference] = 1
            else:
                messages[message.reaction_reference] += 1
        self.reaction_per_message = {
                                     "ordered_mesage_id":sorted(messages, key = messages.get, reverse=True), 
                                     "num_reaction" : messages
                                    }
        
    def get_reaction_sent_per_user(self):
        users = self.db.session.query(distinct(Messages.from_user)).filter(Messages.msg_type == "reaction")
        user_to_reaction = {}
        for user in users:
            user_to_reaction[user[0]] = self.db.session.query(Messages).filter(Messages.msg_type == "reaction").filter(Messages.from_user == user[0]).count()
        self.reaction_sent_per_user = {
                                     "ordered_user":sorted(user_to_reaction, key = user_to_reaction.get, reverse=True), 
                                     "user_to_reaction" : user_to_reaction
                                    }

    def get_reaction_type_popularity(self):
        reaction_messages = self.db.session.query(Messages).filter(Messages.msg_type == "reaction")
        self.reaction_popularity_map = {"reactions":{}}
        for reaction in reaction_messages:
            if reaction.reaction_body not in self.reaction_popularity_map["reactions"]:
                self.reaction_popularity_map["reactions"][reaction.reaction_body] = 1
            else:
                self.reaction_popularity_map["reactions"][reaction.reaction_body] += 1
        self.reaction_popularity_map["sorted"] = sorted(self.reaction_popularity_map["reactions"], key = self.reaction_popularity_map["reactions"].get, reverse=True), 

    def get_reaction_poplarity_per_topic(self):
        pass

    def get_all_user_message_id(self):
        pass

    def get_user_sent_most_reactions(self):
        # Need get_all_user_message_id
        pass

    def get_user_recieved_most_reactions(self):
        # Need get_all_user_message_id
        pass


    def get_reaction_type_popularity_per_user(self):
        # Need get_all_user_message_id
        pass
