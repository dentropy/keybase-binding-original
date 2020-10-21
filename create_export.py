from string import Template
import subprocess
import json
from database import DB, Messages

class ExportKeybase():
    def get_team_channels(self,keybase_team_name):
        get_teams_channels = Template('''
        {
            "method": "listconvsonname",
            "params": {
                "options": {
                    "topic_type": "CHAT",
                    "members_type": "team",
                    "name": "$TEAM_NAME"
                }
            }
        }
        ''')
        dentropydaemon_channels_json = get_teams_channels.substitute(TEAM_NAME=keybase_team_name)
        dentropydaemon_channels = subprocess.run(["keybase", "chat", "api", "-m", dentropydaemon_channels_json],  capture_output=True)
        dentropydaemon_channels = str(dentropydaemon_channels.stdout)[2:-3]
        mah_json = json.loads(dentropydaemon_channels)
        mah_channels = []
        for i in mah_json["result"]["conversations"]:
            mah_channels.append(i["channel"]["topic_name"])
        return mah_channels

    def get_team_chat_channel(self, keybase_team_name, keybase_topic_name):
        get_teams_channels = Template('''
        {
            "method": "read",
            "params": {
                "options": {
                    "channel": {
                        "name": "$TEAM_NAME",
                        "members_type": "team",
                        "topic_name": "$TOPIC_NAME"
                    }
                }
            }
        }
        ''')
        dentropydaemon_channels_json = get_teams_channels.substitute(TEAM_NAME=keybase_team_name, TOPIC_NAME=keybase_topic_name)
        command = ["keybase", "chat", "api", "-m", dentropydaemon_channels_json]
        response = subprocess.check_output(command)
        return json.loads(response.decode('utf-8'))

    def generate_json_export(self, keybase_team, output_file):
        complexity_weekend_teams = self.get_team_channels(keybase_team)
        mah_messages = {"topic_name":{}}
        for topic in complexity_weekend_teams:
            mah_messages["topic_name"][topic] = self.get_team_chat_channel(keybase_team, topic)

        text_file = open(output_file, "w")
        n = text_file.write(json.dumps(mah_messages))
        text_file.close()

    def get_text_messages(self, mah_messages, db):
        for topic in mah_messages["topic_name"]:
            for message in mah_messages["topic_name"][topic]["result"]["messages"]:
                if message["msg"]["content"]["type"] == "text":
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "text",
                        from_user = message["msg"]["sender"]["username"],
                        sent_time = message["msg"]["sent_at"],
                        txt_body =  message["msg"]["content"]["text"]["body"]
                        ))
        db.session.commit()

    def get_reaction_messages(self, mah_messages, db):
        print(mah_messages)
        for topic in mah_messages["topic_name"]:
            for message in mah_messages["topic_name"][topic]["result"]["messages"]:
                if message["msg"]["content"]["type"] == "reaction":
                    root_msg_id = message["msg"]["content"]["reaction"]["m"]
                    root_msg = db.session.query(Messages).filter_by(topic=topic).filter_by(msg_id = root_msg_id)
                    if root_msg.count() == 1:
                        print(root_msg.first().id)
                        print(message["msg"]["content"]["reaction"]["b"])
                        db.session.add( Messages( 
                            team = "complexityweekend.oct2020", 
                            topic = topic,
                            msg_id = message["msg"]["id"],
                            msg_type = "reaction",
                            from_user = message["msg"]["sender"]["username"],
                            sent_time = message["msg"]["sent_at"],
                            reaction_body =  message["msg"]["content"]["reaction"]["b"],
                            reaction_reference = root_msg.first().id
                        ))
        db.session.commit()


    def convert_json_to_sql(self, json_file, sql_connection_string):
        #db = DB("sqlite:///complexityweekend.sqlite")
        db = DB(sql_connection_string)
        #mah_messages = json.load(open('./complexityweekend.json', 'r'))
        mah_messages = json.load(open(json_file, 'r'))
        self.get_text_messages(mah_messages, db)
        self.get_reaction_messages(mah_messages, db)
        print("Conversion from json to sql complete")
        

ex_key = ExportKeybase()
ex_key.generate_json_export("complexweekend.oct2020", "complexityweekend.json")
ex_key.convert_json_to_sql("./complexityweekend.json", "sqlite:///complexityweekend.sqlite")
