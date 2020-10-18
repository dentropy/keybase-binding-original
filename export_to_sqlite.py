import json
from database import session, Messages

mah_messages = json.load(open('/home/dentropy/Documents/Projects/pykeybasebot/json/complexityweekend.json', 'r'))

def get_text_messages():
    for topic in mah_messages["topic_name"]:
        for message in mah_messages["topic_name"][topic]["result"]["messages"]:
            if message["msg"]["content"]["type"] == "text":
                session.add( Messages( 
                    team = "complexityweekend.oct2020", 
                    topic = topic,
                    msg_id = message["msg"]["id"],
                    msg_type = "text",
                    from_user = message["msg"]["sender"]["username"],
                    sent_time = message["msg"]["sent_at"],
                    txt_body =  message["msg"]["content"]["text"]["body"]
                    ))
    session.commit()

def get_reaction_messages():
    print(mah_messages)
    for topic in mah_messages["topic_name"]:
        for message in mah_messages["topic_name"][topic]["result"]["messages"]:
            if message["msg"]["content"]["type"] == "reaction":
                root_msg_id = message["msg"]["content"]["reaction"]["m"]
                root_msg = session.query(Messages).filter_by(topic=topic).filter_by(msg_id = root_msg_id)
                if root_msg.count() == 1:
                    print(root_msg.first().id)
                    print(message["msg"]["content"]["reaction"]["b"])
                    session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "reaction",
                        from_user = message["msg"]["sender"]["username"],
                        sent_time = message["msg"]["sent_at"],
                        reaction_body =  message["msg"]["content"]["reaction"]["b"],
                        reaction_reference = root_msg.first().id
                    ))
    session.commit()
                    
get_text_messages()
get_reaction_messages()
