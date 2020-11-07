from database import DB, Messages
from sqlalchemy import func
import pandas as pd
from sqlalchemy import distinct
from urlextract import URLExtract
from tld import get_fld
import json

class GeneratedAnalytics():
    def __init__(self, db_url):
        """GeneratedAnalytics class constructor."""
        self.db = DB(db_url)
        self.get_list_all_users()
        print("--> from " + str(len(self.user_list)) + " users")
        self.get_list_all_topics()
        print("--> spanning " + str(len(self.topic_list)) + " topics")
        self.get_characters_per_user()
        self.get_characters_per_topic()
        self.get_messages_per_user()
        self.get_messages_per_topic()
        self.get_number_users_per_topic()
        self.get_reaction_per_message()
        self.get_reaction_sent_per_user()
        self.get_reaction_type_popularity()
        self.get_edits_per_user()
        self.get_edits_per_topic()
        self.get_deletes_per_user()
        self.get_deletes_per_topic()
        self.get_who_edits_most_per_capita()
        self.get_who_deletes_most_per_capita()
        self.get_topic_deletes_per_capita()
        self.get_top_domains()
        
        print("Finished initializing analytics object.")
        self.get_topic_edits_per_capita()
        
    def get_message(self, message_id):
        """Returns a single row from Message object (SQL table) by ID."""
        return self.db.session.query(Messages).get(message_id)

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
        self.user_list = []
        for user in individual_users:
            self.user_list.append(user[0])
        return self.user_list

    def get_list_all_topics(self):
        """Update and return list of all topics."""
        individual_topic = self.db.session.query(distinct(Messages.topic))
        self.topic_list = []
        for topic in individual_topic:
            self.topic_list.append(topic[0])
        return self.topic_list

    def get_characters_per_user(self):
        """Update and return total number of characters from messages for each user."""
        characters_per_message = {}
        for user in self.user_list:
            characters_per_message[user] = 0
            user_messages = self.db.session.query(Messages).\
                filter(Messages.txt_body != None).\
                filter_by(from_user=user)
            for message in user_messages:
                characters_per_message[user] += len(message.txt_body)
        list_of_users = sorted(characters_per_message, key = characters_per_message.get, reverse=True)
        self.characters_per_user = {"user": [], "characters_per_user": []}
        for item in list_of_users:
            self.characters_per_user["user"].append(item)
            self.characters_per_user["characters_per_user"].append(characters_per_message[item])
        return self.characters_per_user

    def get_characters_per_topic(self):
        """Update and return total number of characters from messages posted in each topic channel."""
        messages_per_topic = {}
        for topic in self.topic_list:
            messages_per_topic[topic] = 0
            topic_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
            for message in topic_messages:
                messages_per_topic[topic] += len(message.txt_body)
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.characters_per_topic = {"topic": [], "characters_per_topic": []}
        for item in list_of_users:
            self.characters_per_topic["topic"].append(item)
            self.characters_per_topic["characters_per_topic"].append(messages_per_topic[item])
        return self.characters_per_topic

    def get_messages_per_user(self):
        """Update and return total number of messages for each user."""
        messages_per_user = {}
        for user in self.user_list:
            messages_per_user[user] = 0
            user_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(from_user=user)
            messages_per_user[user] = user_messages.count()
        list_of_users = sorted(messages_per_user, key = messages_per_user.get, reverse=True)
        self.messages_per_user = {"user": [], "messages_per_user": []}
        for item in list_of_users:
            self.messages_per_user["user"].append(item)
            self.messages_per_user["messages_per_user"].append(messages_per_user[item])
        return self.messages_per_user

    def get_messages_per_topic(self):
        """Update and return total number of messages posted in each topic."""
        messages_per_topic = {}
        for topic in self.topic_list:
            messages_per_topic[topic] = 0
            topic_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
            messages_per_topic[topic] = topic_messages.count()
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.messages_per_topic = {"topic": [], "messages_per_topic": []}
        for item in list_of_users:
            self.messages_per_topic["topic"].append(item)
            self.messages_per_topic["messages_per_topic"].append(messages_per_topic[item])
        return self.messages_per_topic

    def get_number_users_per_topic(self):
        """Update and return the number of users for each topic."""
        messages_per_topic = {}
        for topic in self.topic_list:
            topic_messages = self.db.session.query(distinct(Messages.from_user)).\
                filter(Messages.txt_body != None).\
                filter_by(topic=topic)
            messages_per_topic[topic] = topic_messages.count()
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        self.number_users_per_topic = {"users_list": [], "topics_list": []}
        for item in list_of_users:
            self.number_users_per_topic["users_list"].append(item)
            self.number_users_per_topic["topics_list"].append(messages_per_topic[item])
        return self.number_users_per_topic


    def get_reaction_per_message(self):
        """Update the reactions to each message."""
        messages = {}
        topic_messages = self.db.session.query(Messages).filter(Messages.msg_type == "reaction")
        for message in topic_messages:
            if message.msg_reference not in messages:
                messages[message.msg_reference] = 1
            else:
                messages[message.msg_reference] += 1
        self.reaction_per_message = {
                                     "ordered_message_id":sorted(messages, key = messages.get, reverse=True), 
                                     "num_reaction" : messages
                                    }
        
    def get_reaction_sent_per_user(self):
        """Update the reactions sent by each user."""
        users = self.db.session.query(distinct(Messages.from_user)).filter(Messages.msg_type == "reaction")
        user_to_reaction = {}
        for user in users:
            user_to_reaction[user[0]] = self.db.session.query(Messages).filter(Messages.msg_type == "reaction").\
                filter(Messages.from_user == user[0]).count()
        self.reaction_sent_per_user = {
                                     "ordered_user":sorted(user_to_reaction, key = user_to_reaction.get, reverse=True), 
                                     "user_to_reaction" : user_to_reaction
                                    }

    def get_reaction_type_popularity(self):
        """Update and return the popularity of all the reaction types."""
        reaction_messages = self.db.session.query(Messages).filter(Messages.msg_type == "reaction")
        self.reaction_popularity_map = {"reactions":{}}
        for reaction in reaction_messages:
            if reaction.reaction_body not in self.reaction_popularity_map["reactions"]:
                self.reaction_popularity_map["reactions"][reaction.reaction_body] = 1
            else:
                self.reaction_popularity_map["reactions"][reaction.reaction_body] += 1
        self.reaction_popularity_map["sorted"] = sorted(self.reaction_popularity_map["reactions"], key = self.reaction_popularity_map["reactions"].get, reverse=True), 

    def get_reaction_poplarity_topic(self, topic):
        """Get popularity of all reactions in a specific topic."""
        reaction_popularity = {"reactions":{}, "list":[]}
        reaction_messages = self.db.session.query(Messages.reaction_body).filter(Messages.topic == topic).\
            filter(Messages.msg_type == "reaction")
        for reaction in reaction_messages:
            if reaction[0] not in reaction_popularity["reactions"]:
                reaction_popularity["reactions"][reaction[0]] = 1
            else:
                reaction_popularity["reactions"][reaction[0]] += 1
        reaction_popularity["list"] = sorted(reaction_popularity["reactions"], key = reaction_popularity["reactions"].get, reverse=True)
        return reaction_popularity

    def get_all_user_message_id(self, user):
        """For a specific user, return all message IDs involving that user."""
        user_messages = {"text":[], "reaction":[], "attachment":[]}
        mah_messages = self.db.session.query(Messages.id).filter(Messages.from_user == user).filter(Messages.msg_type == "text")
        for message in mah_messages:
            user_messages["text"].append(message.id)
        mah_messages = self.db.session.query(Messages.id).filter(Messages.from_user == user).filter(Messages.msg_type == "reaction")
        for message in mah_messages:
            user_messages["reaction"].append(message.id)
        mah_messages = self.db.session.query(Messages.id).filter(Messages.from_user == user).filter(Messages.msg_type == "attachment")
        for message in mah_messages:
            user_messages["attachment"].append(message.id)
        return user_messages

    def get_user_sent_most_reactions(self):
        """Return the sorted user by most number of reactions issued."""
        self.reactions_per_user = {"users_reactions":{}, "users_ordered":[]}
        for user in self.user_list:
            mah_messages = self.db.session.query(Messages.id).filter(Messages.from_user == user).filter(Messages.msg_type == "reaction")
            self.reactions_per_user["users_reactions"][user] = mah_messages.count()
        self.reactions_per_user["users_ordered"] = sorted(self.reactions_per_user["users_reactions"], key = self.reactions_per_user["users_reactions"].get, reverse=True)
        return self.reactions_per_user

    def get_user_recieved_most_reactions(self):
        """Update and return the sorted listing of users by number of reactions received."""
        self.recieved_most_reactions = {"users_reactions":{}, "users_ordered":[]}
        reaction_messages = self.db.session.query(Messages).filter(Messages.msg_type == "reaction")
        for message in reaction_messages:
            mah_message = self.db.session.query(Messages).get(message.msg_reference)
            if mah_message.from_user not in self.recieved_most_reactions["users_reactions"]:
                self.recieved_most_reactions["users_reactions"][mah_message.from_user] = 1
            else:
                self.recieved_most_reactions["users_reactions"][mah_message.from_user] += 1
        self.recieved_most_reactions["users_orderd"] = sorted(self.recieved_most_reactions["users_reactions"], key = self.recieved_most_reactions["users_reactions"].get, reverse=True)
        return self.recieved_most_reactions

                               
    def get_edits_per_user(self):
        """Update and return the number of message edits by user."""
        individual_users = self.db.session.query(distinct(Messages.from_user)).filter(Messages.msg_type == "edit")
        self.edits_per_user = {"users":{}, "ordered_users":[], "ordered_num_edits":[]}
        for user in individual_users:
            tmp_query = self.db.session.query(Messages).filter(Messages.msg_type == "edit").filter(Messages.from_user == user[0])
            self.edits_per_user["users"][user[0]] = tmp_query.count()
        self.edits_per_user["ordered_users"] = sorted(self.edits_per_user["users"], key = self.edits_per_user["users"].get, reverse=True)
        for item in self.edits_per_user["ordered_users"]:
            self.edits_per_user["ordered_num_edits"].append(self.edits_per_user["users"][item])
        return self.edits_per_user
    
    def get_edits_per_topic(self):
        """Update and return the raw number of edited message by topic."""
        individual_topics = self.db.session.query(distinct(Messages.topic)).filter(Messages.msg_type == "edit")
        self.edits_per_topic = {"topics":{}, "ordered_topics":[], "ordered_num_edits":[]}
        for topic in individual_topics:
            tmp_query = self.db.session.query(Messages).filter(Messages.msg_type == "edit").filter(Messages.topic == topic[0])
            self.edits_per_topic["topics"][topic[0]] = tmp_query.count()
        self.edits_per_topic["ordered_topics"] = sorted(self.edits_per_topic["topics"], key = self.edits_per_topic["topics"].get, reverse=True)
        for item in self.edits_per_topic["ordered_topics"]:
            self.edits_per_topic["ordered_num_edits"].append(self.edits_per_topic["topics"][item])
        return self.edits_per_topic

    def get_deletes_per_user(self):
        """Update and return the raw number of deleted messages by user."""
        individual_users = self.db.session.query(distinct(Messages.from_user)).filter(Messages.msg_type == "delete")
        self.deletes_per_user = {"users":{}, "ordered_users":[], "ordered_num_deletes":[]}
        for user in individual_users:
            tmp_query = self.db.session.query(Messages).filter(Messages.msg_type == "delete").filter(Messages.from_user == user[0])
            self.deletes_per_user["users"][user[0]] = tmp_query.count()
        self.deletes_per_user["ordered_users"] = sorted(self.deletes_per_user["users"], key = self.deletes_per_user["users"].get, reverse=True)
        for item in self.deletes_per_user["ordered_users"]:
            self.deletes_per_user["ordered_num_deletes"].append(self.deletes_per_user["users"][item])
        return self.deletes_per_user


    def get_deletes_per_topic(self):
        """Update and return the raw number of deleted messages by topic."""
        individual_topics = self.db.session.query(distinct(Messages.topic)).filter(Messages.msg_type == "delete")
        self.deletes_per_topic = {"topics":{}, "ordered_topics":[], "ordered_num_deletes":[]}
        for topic in individual_topics:
            tmp_query = self.db.session.query(Messages).filter(Messages.msg_type == "delete").filter(Messages.topic == topic[0])
            self.deletes_per_topic["topics"][topic[0]] = tmp_query.count()
        self.deletes_per_topic["ordered_topics"] = sorted(self.deletes_per_topic["topics"], key = self.deletes_per_topic["topics"].get, reverse=True)
        for item in self.deletes_per_topic["ordered_topics"]:
            self.deletes_per_topic["ordered_num_deletes"].append(self.deletes_per_topic["topics"][item])
        return self.deletes_per_topic
    

    def get_who_edits_most_per_capita(self):
        """Update and return the per-capita message edits by user."""
        self.who_edits_most_per_capita = {"users":{}, "ordered_users":[], "ordered_edit_per_capita" : []}
        for user in self.user_list:
            mah_metadata = self.get_num_messages_from_user(user)
            if mah_metadata['edit'] != 0 and mah_metadata['text'] != 0:     
                self.who_edits_most_per_capita["users"][user] = mah_metadata['edit'] / mah_metadata['text'] * 100 
            else:
                self.who_edits_most_per_capita["users"][user] = 0
        self.who_edits_most_per_capita["ordered_users"] = sorted(self.who_edits_most_per_capita["users"], key = self.who_edits_most_per_capita["users"].get, reverse=True)
        for user in self.who_edits_most_per_capita["ordered_users"]:
            self.who_edits_most_per_capita["ordered_edit_per_capita"].append(self.who_edits_most_per_capita["users"][user])
        return self.who_edits_most_per_capita

    def get_who_deletes_most_per_capita(self):
        """Update and return the per-capita message deletions by user."""
        self.who_deletes_most_per_capita = {"users":{}, "ordered_users":[], "ordered_edit_per_capita" : []}
        for user in self.user_list:
            mah_metadata = self.get_num_messages_from_user(user)
            if mah_metadata['delete'] != 0 and mah_metadata['text'] != 0:     
                self.who_deletes_most_per_capita["users"][user] = mah_metadata['delete'] / mah_metadata['text'] * 100 
            else:
                self.who_deletes_most_per_capita["users"][user] = 0
        self.who_deletes_most_per_capita["ordered_users"] = sorted(self.who_deletes_most_per_capita["users"], key = self.who_deletes_most_per_capita["users"].get, reverse=True)
        for user in self.who_deletes_most_per_capita["ordered_users"]:
            self.who_deletes_most_per_capita["ordered_edit_per_capita"].append(self.who_deletes_most_per_capita["users"][user])
        return self.who_deletes_most_per_capita

    def get_topic_edits_per_capita(self):
        """Update and return the per-capita edits by topic."""
        self.topic_edits_per_capita = {"topics":{}, "ordered_topics":[], "ordered_edit_per_capita" : []}
        for user in self.topic_list:
            mah_metadata = self.get_num_messages_from_topic(user)
            if mah_metadata['edit'] != 0:     
                self.topic_edits_per_capita["topics"][user] = mah_metadata['edit'] / mah_metadata['text'] * 100 
            else:
                self.topic_edits_per_capita["topics"][user] = 0
        self.topic_edits_per_capita["ordered_topics"] = sorted(self.topic_edits_per_capita["topics"], key = self.topic_edits_per_capita["topics"].get, reverse=True)
        for user in self.topic_edits_per_capita["ordered_topics"]:
            self.topic_edits_per_capita["ordered_edit_per_capita"].append(self.topic_edits_per_capita["topics"][user])
        return self.topic_edits_per_capita
    
    def get_topic_deletes_per_capita(self):
        """Update and return the per-capita deletes by topic."""
        self.topic_deletes_per_capita = {"topics":{}, "ordered_topics":[], "ordered_edit_per_capita" : []}
        for user in self.topic_list:
            mah_metadata = self.get_num_messages_from_topic(user)
            if mah_metadata['edit'] != 0:     
                self.topic_deletes_per_capita["topics"][user] = mah_metadata['edit'] / mah_metadata['text'] * 100 
            else:
                self.topic_deletes_per_capita["topics"][user] = 0
        self.topic_deletes_per_capita["ordered_topics"] = sorted(self.topic_deletes_per_capita["topics"], key = self.topic_deletes_per_capita["topics"].get, reverse=True)
        for user in self.topic_deletes_per_capita["ordered_topics"]:
            self.topic_deletes_per_capita["ordered_edit_per_capita"].append(self.topic_deletes_per_capita["topics"][user])
        return self.topic_deletes_per_capita

    def get_top_domains(self):
        """Update list of most-popular top-level domains linked in text chat."""
        mah_urls = []
        for url in self.db.session.query(Messages).filter(Messages.urls != None):
            for actual_url in json.loads(url.urls): 
                mah_urls.append(actual_url)
        self.top_domains = {"URLs":{}}
        for url in mah_urls:
            try:
                tmp_url =  get_fld(url)
                if tmp_url not in self.top_domains["URLs"]:
                    self.top_domains["URLs"][tmp_url] = 1
                else:
                    self.top_domains["URLs"][tmp_url] += 1
            except:
                if url not in self.top_domains["URLs"]:
                    self.top_domains["URLs"][url] = 0
                else:
                    self.top_domains["URLs"][url] += 1
                self.top_domains["URLs"][url] += 1
        self.top_domains["top_domains_sorted"] = sorted(self.top_domains["URLs"], key = self.top_domains["URLs"].get, reverse=True)
        self.top_domains["num_times_repeated"] = []
        for url in self.top_domains["top_domains_sorted"]:
            self.top_domains["num_times_repeated"].append(self.top_domains["URLs"][url])
    
    
    def get_reaction_type_popularity_per_user(self, user):
        """Returns/updates the popularity of a given reaction type by their username"""
        user_used_reactions = {"users_reactions":{}, "reactions_ordered":[]}
        mah_reactions = self.db.session.query(Messages).filter(Messages.from_user == user).filter(Messages.msg_type == "reaction")
        for reaction in mah_reactions:
            if reaction.reaction_body not in user_used_reactions["users_reactions"]:
                user_used_reactions["users_reactions"][reaction.reaction_body] = 1
            else:
                user_used_reactions["users_reactions"][reaction.reaction_body] += 1
        user_used_reactions["reactions_ordered"] = sorted(user_used_reactions["users_reactions"], key = user_used_reactions["users_reactions"].get, reverse=True)
        return user_used_reactions

    def get_user_ids(self, user):
        """Get ID of a given user."""
        pass
    
    def get_message_data_frames(self, offset_time=0):
        """Return Pandas data frame table."""
        text_messages = self.db.session.query(Messages).filter(Messages.msg_type == "text")
        message_data = {
            "user": [],
            "msg_id": [],
            "time": [],
            "team": [],
            "topic": [],
            "text": [],
            "word_count": []
        }
        cu = pd.DataFrame(data=self.get_characters_per_user())
        mu = pd.DataFrame(data=self.get_messages_per_user())
        ct = pd.DataFrame(data=self.get_characters_per_topic())
        mt = pd.DataFrame(data=self.get_messages_per_topic())
        for msg in text_messages:
            message_data["user"].append(msg.from_user)
            message_data["msg_id"].append(msg.msg_id)
            message_data["time"].append(msg.sent_time-offset_time)
            message_data["team"].append(msg.team)
            message_data["topic"].append(msg.topic)
            message_data["text"].append(msg.txt_body)
            message_data["word_count"].append(msg.word_count)
        df = pd.DataFrame(data=message_data)
        df = pd.merge(df, cu, on="user", how="left")
        df = pd.merge(df, mu, on="user", how="left")
        df = pd.merge(df, ct, on="topic", how="left")
        pandas_table = pd.merge(df, mt, on="topic", how="left")
        return pandas_table

