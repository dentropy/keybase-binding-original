'''
* Total number of characters typed per
  * User
  * Channel
'''
from database import DB, Messages
from sqlalchemy import func
from sqlalchemy import distinct

db = DB("sqlite:///complexityweekend.sqlite")

def get_list_all_users():
    individual_users = db.session.query(distinct(Messages.from_user))
    user_list = []
    for user in individual_users:
        user_list.append(user[0])
    return user_list

def get_list_all_topics():
    individual_topic = db.session.query(distinct(Messages.topic))
    topic_list = []
    for topic in individual_topic:
        topic_list.append(topic[0])
    return topic_list

def get_characters_per_user(user_list):
    messages_per_user = {}
    for user in user_list:
        messages_per_user[user] = 0
        user_messages = db.session.query(Messages).filter(Messages.txt_body != None).filter_by(from_user=user)
        for message in user_messages:
            messages_per_user[user] += len(message.txt_body)
    list_of_users = sorted(messages_per_user, key = messages_per_user.get, reverse=True)
    output_format = []
    for item in list_of_users:
        output_format.append([item, messages_per_user[item]])
    return output_format
  
def get_characters_per_topic(topic_list):
    messages_per_topic = {}
    for topic in topic_list:
        messages_per_topic[topic] = 0
        topic_messages = db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
        for message in topic_messages:
            messages_per_topic[topic] += len(message.txt_body)
    list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
    output_format = []
    for item in list_of_users:
        output_format.append([item, messages_per_topic[item]])
    return output_format

'''
* Total number of messages per
  * user
  * Channel
'''

def get_messages_per_user(user_list):
    messages_per_user = {}
    for user in user_list:
        messages_per_user[user] = 0
        user_messages = db.session.query(Messages).filter(Messages.txt_body != None).filter_by(from_user=user)
        messages_per_user[user] = user_messages.count()
    list_of_users = sorted(messages_per_user, key = messages_per_user.get, reverse=True)
    output_format = []
    for item in list_of_users:
        output_format.append([item, messages_per_user[item]])
    return output_format

def get_messages_per_topic(topic_list):
    messages_per_topic = {}
    for topic in topic_list:
        messages_per_topic[topic] = 0
        topic_messages = db.session.query(Messages).filter(Messages.txt_body != None).filter_by(topic=topic)
        messages_per_topic[topic] = topic_messages.count()
    list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
    output_format = []
    for item in list_of_users:
        output_format.append([item, messages_per_topic[item]])
    return output_format

def get_number_users_per_topic(topic_list):
    messages_per_topic = {}
    for topic in topic_list:
        topic_messages = db.session.query(distinct(Messages.from_user)).filter(Messages.txt_body != None).filter_by(topic=topic)
        messages_per_topic[topic] = topic_messages.count()
    list_of_users = sorted(messages_per_topic, key = messages_per_topic.get, reverse=True)
    output_format = []
    for item in list_of_users:
        output_format.append([item, messages_per_topic[item]])
    return output_format

'''
user_list = get_list_all_users()
topic_list = get_list_all_topics()
characters_per_user = get_characters_per_user(user_list)
character_per_topic = get_characters_per_topic(topic_list)
messages_per_user = get_messages_per_user(user_list)
messages_per_topic = get_messages_per_topic(topic_list)
number_users_per_topic = get_number_users_per_topic(topic_list)
print(user_list)
print(topic_list)
print(characters_per_user)
print(character_per_topic)
print(messages_per_topic)
print(number_users_per_topic)
'''