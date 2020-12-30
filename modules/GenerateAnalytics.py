from database import DB, Messages
from sqlalchemy import func, asc
import pandas as pd
from datetime import *
from sqlalchemy import distinct
from urlextract import URLExtract
from tld import get_fld
import json
import pprint
class GenerateAnalytics():
    def __init__(self, db_url):
        """GeneratedAnalytics class constructor."""
        self.db = DB(db_url)
        self.user_list = self.get_list_all_users()
        self.topic_list = self.get_list_all_topics()
        
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

    def get_characters_per_user(self):
        """Update and return total number of characters from messages for each user."""
        store_message_state = {}
        characters_per_user = {
            "type":"Show X Axis",
            "x_label":"user",
            "y_label":"characters_per_user",
            "x_axis":[],
            "y_axis":[]
        }
        for user in self.user_list:
            store_message_state[user] = 0
            user_messages = self.db.session.query(Messages).\
                filter(Messages.txt_body != None).\
                filter_by(from_user=user)
            for message in user_messages:
                store_message_state[user] += len(message.txt_body)
        list_of_users = sorted(store_message_state, key = store_message_state.get, reverse=True)
        for item in list_of_users:
            characters_per_user["x_axis"].append(item)
            characters_per_user["y_axis"].append(store_message_state[item])
        characters_per_user["title"] = "Characters Per User, Num Users = " + str(len(characters_per_user["x_axis"]))
        return characters_per_user

    def get_characters_per_topic(self):
        """Update and return total number of characters from messages posted in each topic channel."""
        messages_per_topic = {}
        for topic in self.topic_list:
            messages_per_topic[topic] = 0
            topic_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
            for message in topic_messages:
                messages_per_topic[topic] += len(message.txt_body)
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        characters_per_topic = {
            "type":"Show X Axis",
            "x_label":"topic",
            "y_label":"characters_per_topic",
            "x_axis":[],
            "y_axis":[],
            "title": "Messages Per Topic, Num Topics = " + str(len(messages_per_topic))
        }
        for item in list_of_users:
            characters_per_topic["x_axis"].append(item)
            characters_per_topic["y_axis"].append(messages_per_topic[item])
        return characters_per_topic

    def get_messages_per_user(self):
        """Update and return total number of messages for each user."""
        tmp_messages_per_user = {}
        for user in self.user_list:
            tmp_messages_per_user[user] = 0
            user_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(from_user=user)
            tmp_messages_per_user[user] = user_messages.count()
        list_of_users = sorted(tmp_messages_per_user, key = tmp_messages_per_user.get, reverse=True)
        messages_per_user = {"user": [], "messages_per_user": []}
        for item in list_of_users:
            messages_per_user["user"].append(item)
            messages_per_user["messages_per_user"].append(tmp_messages_per_user[item])
        graph_characters_per_topic = {
            "type":"Show X Axis",
            "x_label":"user",
            "y_label":"messages_per_user",
            "x_axis":messages_per_user["user"],
            "y_axis":messages_per_user["messages_per_user"],
            "title": "Messages Per User, Num Users = " + str(len(messages_per_user["messages_per_user"]))
        }
        return graph_characters_per_topic

    def get_messages_per_topic(self):
        """Update and return total number of messages posted in each topic."""
        tmp_messages_per_topic = {}
        for topic in self.topic_list:
            tmp_messages_per_topic[topic] = 0
            topic_messages = self.db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
            tmp_messages_per_topic[topic] = topic_messages.count()
        list_of_users = sorted(tmp_messages_per_topic, key = tmp_messages_per_topic.get, reverse=True)
        messages_per_topic = {"topic": [], "messages_per_topic": []}
        for item in list_of_users:
            messages_per_topic["topic"].append(item)
            messages_per_topic["messages_per_topic"].append(tmp_messages_per_topic[item])
        graph_messages_per_topic = {
            "type":"Show X Axis",
            "x_label":"topic",
            "y_label":"messages_per_topic",
            "x_axis":messages_per_topic["topic"],
            "y_axis":messages_per_topic["messages_per_topic"],
            "title": "Messages Per Topic, Num Topics = " + str(len(messages_per_topic["topic"]))
        }
        return graph_messages_per_topic

    def get_number_users_per_topic(self):
        """Update and return the number of users for each topic."""
        messages_per_topic = {}
        for topic in self.topic_list:
            topic_messages = self.db.session.query(distinct(Messages.from_user)).\
                filter(Messages.txt_body != None).\
                filter_by(topic=topic)
            messages_per_topic[topic] = topic_messages.count()
        list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
        number_users_per_topic = {"users_list": [], "topics_list": []}
        for item in list_of_users:
            number_users_per_topic["users_list"].append(item)
            number_users_per_topic["topics_list"].append(messages_per_topic[item])
        graph_number_users_per_topic = {
            "type":"Show X Axis",
            "x_label":"users_list",
            "y_label":"topics_list",
            "x_axis":number_users_per_topic["users_list"],
            "y_axis":number_users_per_topic["topics_list"],
            "title": "Number of User per Topic, Num Topics = " + str(len(number_users_per_topic["topics_list"]))
        }
        return graph_number_users_per_topic

    # TODO Move this functon somewhere else
    def get_reaction_per_message(self):
        """Update the reactions to each message."""
        messages = {}
        topic_messages = self.db.session.query(Messages).filter(Messages.msg_type == "reaction")
        for message in topic_messages:
            if message.msg_reference not in messages:
                messages[message.msg_reference] = 1
            else:
                messages[message.msg_reference] += 1
        reaction_per_message = {
                                     "ordered_message_id":sorted(messages, key = messages.get, reverse=True), 
                                     "num_reaction" : messages
                                    }
        return reaction_per_message
        
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
        return self.reaction_sent_per_user

    def get_reaction_type_popularity(self):
        """Update and return the popularity of all the reaction types."""
        reaction_messages = self.db.session.query(Messages).filter(Messages.msg_type == "reaction")
        reaction_popularity_map = {"reactions":{}}
        for reaction in reaction_messages:
            if reaction.reaction_body not in reaction_popularity_map["reactions"]:
                reaction_popularity_map["reactions"][reaction.reaction_body] = 1
            else:
                reaction_popularity_map["reactions"][reaction.reaction_body] += 1
        reaction_popularity_map["sorted"] = sorted(reaction_popularity_map["reactions"], key = reaction_popularity_map["reactions"].get, reverse=True)
        y_axis = []
        for item in reaction_popularity_map["sorted"]:
            y_axis.append(reaction_popularity_map["reactions"][item])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"reaction",
            "y_label":"number of times reaction used",
            "x_axis":reaction_popularity_map["sorted"],
            "y_axis":y_axis,
            "title": "Reaction Popularity"
        }
        return graph_data

    # TODO Move this somewhere else, or make it more generalized
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

    # Move this somewhere else
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
        reactions_per_user = {"users_reactions":{}, "users_ordered":[]}
        for user in self.user_list:
            mah_messages = self.db.session.query(Messages.id).filter(Messages.from_user == user).filter(Messages.msg_type == "reaction")
            reactions_per_user["users_reactions"][user] = mah_messages.count()
        reactions_per_user["users_ordered"] = sorted(
            reactions_per_user["users_reactions"], 
            key = reactions_per_user["users_reactions"].get, 
            reverse=True)
        y_axis = []
        for item in reactions_per_user["users_ordered"]:
            y_axis.append(reactions_per_user["users_reactions"][item])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users Ordered",
            "y_label":"Num Reactions",
            "x_axis": reactions_per_user["users_ordered"],
            "y_axis":y_axis,
            "title": "Users Who Sent Most Reactions, Num Users = " +  str(len(reactions_per_user["users_reactions"]))
        }
        return graph_data

    def get_user_recieved_most_reactions(self):
        """Update and return the sorted listing of users by number of reactions received."""
        recieved_most_reactions = {"users_reactions":{}, "users_ordered":[]}
        reaction_messages = self.db.session.query(Messages).filter(Messages.msg_type == "reaction")
        for message in reaction_messages:
            mah_message = self.db.session.query(Messages).get(message.msg_reference)
            if mah_message.from_user not in recieved_most_reactions["users_reactions"]:
                recieved_most_reactions["users_reactions"][mah_message.from_user] = 1
            else:
                recieved_most_reactions["users_reactions"][mah_message.from_user] += 1
        recieved_most_reactions["users_ordered"] = sorted(
            recieved_most_reactions["users_reactions"], 
            key = recieved_most_reactions["users_reactions"].get, 
            reverse=True)
        y_axis = []
        for item in recieved_most_reactions["users_ordered"]:
            y_axis.append(recieved_most_reactions["users_reactions"][item])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users Ordered",
            "y_label":"Num Reactions",
            "x_axis": recieved_most_reactions["users_ordered"],
            "y_axis": y_axis,
            "title": "Users Recieved Most Reactions, Num Users = " +  str(len(recieved_most_reactions["users_reactions"]))
        }
        return graph_data

                               
    def get_edits_per_user(self):
        """Update and return the number of message edits by user."""
        individual_users = self.db.session.query(distinct(Messages.from_user)).filter(Messages.msg_type == "edit")
        edits_per_user = {"users":{}, "ordered_users":[], "ordered_num_edits":[]}
        for user in individual_users:
            tmp_query = self.db.session.query(Messages).filter(Messages.msg_type == "edit").filter(Messages.from_user == user[0])
            edits_per_user["users"][user[0]] = tmp_query.count()
        edits_per_user["ordered_users"] = sorted(edits_per_user["users"], key = edits_per_user["users"].get, reverse=True)
        for item in edits_per_user["ordered_users"]:
            edits_per_user["ordered_num_edits"].append(edits_per_user["users"][item])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Num Edits",
            "x_axis": edits_per_user["ordered_users"],
            "y_axis": edits_per_user["ordered_num_edits"],
            "title": "Edits Per User, Num Users = " +  str(len(edits_per_user["ordered_users"]))
        }
        return graph_data
    
    def get_edits_per_topic(self):
        """Update and return the raw number of edited message by topic."""
        individual_topics = self.db.session.query(distinct(Messages.topic)).filter(Messages.msg_type == "edit")
        edits_per_topic = {"topics":{}, "ordered_topics":[], "ordered_num_edits":[]}
        for topic in individual_topics:
            tmp_query = self.db.session.query(Messages).filter(Messages.msg_type == "edit").filter(Messages.topic == topic[0])
            edits_per_topic["topics"][topic[0]] = tmp_query.count()
        edits_per_topic["ordered_topics"] = sorted(edits_per_topic["topics"], key = edits_per_topic["topics"].get, reverse=True)
        for item in edits_per_topic["ordered_topics"]:
            edits_per_topic["ordered_num_edits"].append(edits_per_topic["topics"][item])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Num Edits",
            "x_axis": edits_per_topic["ordered_topics"],
            "y_axis": edits_per_topic["ordered_num_edits"],
            "title": "Edits Per Topic, Num Topics = " +  str(len(edits_per_topic["ordered_topics"]))
        }
        return graph_data

    def get_deletes_per_user(self):
        """Update and return the raw number of deleted messages by user."""
        individual_users = self.db.session.query(distinct(Messages.from_user)).filter(Messages.msg_type == "delete")
        deletes_per_user = {"users":{}, "ordered_users":[], "ordered_num_deletes":[]}
        for user in individual_users:
            tmp_query = self.db.session.query(Messages).filter(Messages.msg_type == "delete").filter(Messages.from_user == user[0])
            deletes_per_user["users"][user[0]] = tmp_query.count()
        deletes_per_user["ordered_users"] = sorted(deletes_per_user["users"], key = deletes_per_user["users"].get, reverse=True)
        for item in deletes_per_user["ordered_users"]:
            deletes_per_user["ordered_num_deletes"].append(deletes_per_user["users"][item])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Num Edits",
            "x_axis": deletes_per_user["ordered_users"],
            "y_axis": deletes_per_user["ordered_num_deletes"],
            "title": "Deletes Per User, Num Users = " +  str(len(deletes_per_user["ordered_users"]))
        }
        return graph_data


    def get_deletes_per_topic(self):
        """Update and return the raw number of deleted messages by topic."""
        individual_topics = self.db.session.query(distinct(Messages.topic)).filter(Messages.msg_type == "delete")
        deletes_per_topic = {"topics":{}, "ordered_topics":[], "ordered_num_deletes":[]}
        for topic in individual_topics:
            tmp_query = self.db.session.query(Messages).filter(Messages.msg_type == "delete").filter(Messages.topic == topic[0])
            deletes_per_topic["topics"][topic[0]] = tmp_query.count()
        deletes_per_topic["ordered_topics"] = sorted(deletes_per_topic["topics"], key = deletes_per_topic["topics"].get, reverse=True)
        for item in deletes_per_topic["ordered_topics"]:
            deletes_per_topic["ordered_num_deletes"].append(deletes_per_topic["topics"][item])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Num Edits",
            "x_axis": deletes_per_topic["ordered_topics"],
            "y_axis": deletes_per_topic["ordered_num_deletes"],
            "title": "Deletes Per Topic, Num Topics = " +  str(len(deletes_per_topic["ordered_topics"]))
        }
        return graph_data
    

    def get_who_edits_most_per_capita(self):
        """Update and return the per-capita message edits by user."""
        who_edits_most_per_capita = {"users":{}, "ordered_users":[], "ordered_edit_per_capita" : []}
        for user in self.user_list:
            mah_metadata = self.get_num_messages_from_user(user)
            if mah_metadata['edit'] != 0 and mah_metadata['text'] != 0:     
                who_edits_most_per_capita["users"][user] = mah_metadata['edit'] / mah_metadata['text'] * 100 
            else:
                who_edits_most_per_capita["users"][user] = 0
        who_edits_most_per_capita["ordered_users"] = sorted(who_edits_most_per_capita["users"], key = who_edits_most_per_capita["users"].get, reverse=True)
        for user in who_edits_most_per_capita["ordered_users"]:
            who_edits_most_per_capita["ordered_edit_per_capita"].append(who_edits_most_per_capita["users"][user])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Edits Per Capita, Percentage",
            "x_axis": who_edits_most_per_capita["ordered_users"],
            "y_axis": who_edits_most_per_capita["ordered_edit_per_capita"],
            "title": "User Edits Per Capita, Num Users = " +  str(len(who_edits_most_per_capita["ordered_users"]))
        }
        return graph_data

    def get_who_deletes_most_per_capita(self):
        """Update and return the per-capita message deletions by user."""
        who_deletes_most_per_capita = {"users":{}, "ordered_users":[], "ordered_edit_per_capita" : []}
        for user in self.user_list:
            mah_metadata = self.get_num_messages_from_user(user)
            if mah_metadata['delete'] != 0 and mah_metadata['text'] != 0:     
                who_deletes_most_per_capita["users"][user] = mah_metadata['delete'] / mah_metadata['text'] * 100 
            else:
                who_deletes_most_per_capita["users"][user] = 0
        who_deletes_most_per_capita["ordered_users"] = sorted(
            who_deletes_most_per_capita["users"], 
            key = who_deletes_most_per_capita["users"].get, 
            reverse=True)
        for user in who_deletes_most_per_capita["ordered_users"]:
            who_deletes_most_per_capita["ordered_edit_per_capita"].append(who_deletes_most_per_capita["users"][user])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Deletes Per Capita, Percentage",
            "x_axis": who_deletes_most_per_capita["ordered_users"],
            "y_axis": who_deletes_most_per_capita["ordered_edit_per_capita"],
            "title": "User Deletes Per Capita, Num Users = " +  str(len(who_deletes_most_per_capita["ordered_users"]))
        }
        return graph_data

    def get_topic_edits_per_capita(self):
        """Update and return the per-capita edits by topic."""
        topic_edits_per_capita = {"topics":{}, "ordered_topics":[], "ordered_edit_per_capita" : []}
        for user in self.topic_list:
            mah_metadata = self.get_num_messages_from_topic(user)
            if mah_metadata['edit'] != 0:     
                topic_edits_per_capita["topics"][user] = mah_metadata['edit'] / mah_metadata['text'] * 100 
            else:
                topic_edits_per_capita["topics"][user] = 0
        topic_edits_per_capita["ordered_topics"] = sorted(topic_edits_per_capita["topics"], key = topic_edits_per_capita["topics"].get, reverse=True)
        for user in topic_edits_per_capita["ordered_topics"]:
            topic_edits_per_capita["ordered_edit_per_capita"].append(topic_edits_per_capita["topics"][user])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Deletes Per Capita, Percentage",
            "x_axis": topic_edits_per_capita["ordered_topics"],
            "y_axis": topic_edits_per_capita["ordered_edit_per_capita"],
            "title": "Topic Edits Per Capita, Num Topics = " +  str(len(topic_edits_per_capita["ordered_topics"]))
        }
        return graph_data
    
    def get_topic_deletes_per_capita(self):
        """Update and return the per-capita deletes by topic."""
        topic_deletes_per_capita = {"topics":{}, "ordered_topics":[], "ordered_edit_per_capita" : []}
        for user in self.topic_list:
            mah_metadata = self.get_num_messages_from_topic(user)
            if mah_metadata['edit'] != 0:     
                topic_deletes_per_capita["topics"][user] = mah_metadata['edit'] / mah_metadata['text'] * 100 
            else:
                topic_deletes_per_capita["topics"][user] = 0
        topic_deletes_per_capita["ordered_topics"] = sorted(topic_deletes_per_capita["topics"], key = topic_deletes_per_capita["topics"].get, reverse=True)
        for user in topic_deletes_per_capita["ordered_topics"]:
            topic_deletes_per_capita["ordered_edit_per_capita"].append(topic_deletes_per_capita["topics"][user])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Deletes Per Capita, Percentage",
            "x_axis": topic_deletes_per_capita["ordered_topics"],
            "y_axis": topic_deletes_per_capita["ordered_edit_per_capita"],
            "title": "Topic Deletes Per Capita, Num Topics = " +  str(len(topic_deletes_per_capita["ordered_topics"]))
        }
        return graph_data

    # TODO Move this method somewhere else
    def get_top_domains(self):
        """Update list of most-popular top-level domains linked in text chat."""
        mah_urls = []
        for url in self.db.session.query(Messages).filter(Messages.urls != None):
            for actual_url in json.loads(url.urls): 
                mah_urls.append(actual_url)
        top_domains = {"URLs":{}}
        for url in mah_urls:
            try:
                tmp_url =  get_fld(url)
                if tmp_url not in top_domains["URLs"]:
                    top_domains["URLs"][tmp_url] = 1
                else:
                    top_domains["URLs"][tmp_url] += 1
            except:
                if url not in top_domains["URLs"]:
                    top_domains["URLs"][url] = 0
                else:
                    top_domains["URLs"][url] += 1
                top_domains["URLs"][url] += 1
        top_domains["top_domains_sorted"] = sorted(top_domains["URLs"], key = top_domains["URLs"].get, reverse=True)
        top_domains["num_times_repeated"] = []
        for url in top_domains["top_domains_sorted"]:
            top_domains["num_times_repeated"].append(top_domains["URLs"][url])
    
    # This needs to be in a seperate class, an interactive one
    def get_reaction_type_popularity_per_user(self, user):
        """Returns/updates the popularity of a given reaction type by their username"""
        user_used_reactions = {"users_reactions":{}, "reactions_ordered":[]}
        mah_reactions = self.db.session.query(Messages).filter(Messages.from_user == user).filter(Messages.msg_type == "reaction")
        for reaction in mah_reactions:
            if reaction.reaction_body not in user_used_reactions["users_reactions"]:
                user_used_reactions["users_reactions"][reaction.reaction_body] = 1
            else:
                user_used_reactions["users_reactions"][reaction.reaction_body] += 1
        user_used_reactions["reactions_ordered"] = sorted(
            user_used_reactions["users_reactions"],
            key = user_used_reactions["users_reactions"].get, 
            reverse=True)
        y_axis = []
        for item in user_used_reactions["reactions_ordered"]:
            y_axis.append(user_used_reactions["users_reactions"][item])
        graph_data = {
            "type":"Show X Axis",
            "x_label":"Users",
            "y_label":"Deletes Per Capita, Percentage",
            "x_axis": user_used_reactions["reactions_ordered"],
            "y_axis": y_axis,
            "title": "Reaction Type Popularity Per User, Num Users = " +  str(len(user_used_reactions["users_reactions"]))
        }
        return graph_data

    # TODO Get rid of this, or provide a comment on why it exists
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
            message_data["time"].append((msg.sent_time - datetime(1970, 1, 1)).total_seconds()-offset_time)
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

class GeneratedAnalytics(GenerateAnalytics):
    def __init__(self, db_url):
        self.db = DB(db_url)
        self.user_list = self.get_list_all_users()
        self.topic_list = self.get_list_all_topics()
        # Same as above constructor so far
        self.characters_per_user = self.get_characters_per_user()
        self.characters_per_topic = self.get_characters_per_topic()
        self.messages_per_user = self.get_messages_per_user()
        self.messages_per_topic = self.get_messages_per_topic()
        self.number_users_per_topic = self.get_number_users_per_topic()
        self.reaction_per_message = self.get_reaction_per_message()
        self.reaction_sent_per_user = self.get_reaction_sent_per_user()
        self.reaction_type_popularity = self.get_reaction_type_popularity()
        self.user_sent_most_reactions = self.get_user_sent_most_reactions()
        self.user_recieved_most_reactions = self.get_user_recieved_most_reactions()
        self.edits_per_user = self.get_edits_per_user()
        self.edits_per_topic = self.get_edits_per_topic()
        self.deletes_per_user = self.get_deletes_per_user()
        self.deletes_per_topic = self.get_deletes_per_topic()
        self.top_domains = self.get_top_domains()
        self.who_edits_most_per_capita = self.get_who_edits_most_per_capita()
        self.who_deletes_most_per_capita = self.get_who_deletes_most_per_capita()
        self.topic_edits_per_capita = self.get_topic_edits_per_capita()
        self.topic_deletes_per_capita = self.get_topic_deletes_per_capita()
        print("Finished initializing analytics object.")