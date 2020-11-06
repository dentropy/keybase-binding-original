from string import Template
import subprocess
import json
from database import DB, Messages
from urlextract import URLExtract

class ExportKeybase():
    def __init__(self):
        self.extractor = URLExtract()
    
    def get_teams(self):
        keybase_teams = subprocess.run(["keybase", "team", "list-memberships"], capture_output=True)
        team_string = str(keybase_teams.stdout).split("\\n")
        teams = []
        for i in team_string[1:-1]:
            teams.append(i.split()[0])
        return teams

    def get_team_memberships(self, team_name):
        json_string = '''
        {
            "method": "list-team-memberships",
            "params": {
                "options": {
                    "team": "%s"
                }
            }
        }
        ''' % (team_name)
        response = subprocess.check_output(["keybase", "team", "api", "-m", json_string])
        user_data = json.loads(response.decode('utf-8'))
        usernames = []
        for key in user_data["result"]["members"].keys():
            if user_data["result"]["members"][key] != None:
                for mah_val in range(len(user_data["result"]["members"][key])):
                    usernames.append(user_data["result"]["members"][key][mah_val]["username"])
        return usernames
    
    def get_user_metadata(self, username):
        user_metadata = {"verification":[]}
        response = subprocess.run(["keybase", "id", username],  capture_output=True).stderr
        response_string = response.decode("utf-8")
        for line in response_string.split("\n"):
            print(line)
            print("**********")
            if "admin of" in line:
                print(line)
                user_metadata["verification"].append(line.split()[6][5:-6])
        for url in self.extractor.find_urls(response_string):
            user_metadata["verification"].append(url)
        json_string = '''
        {
            "method": "list-user-memberships", 
            "params": {
                "options": {"username": "%s"}
            }
        }
        ''' % (username)
        response = json.loads(subprocess.check_output(["keybase", "team", "api", "-m", json_string]).decode('utf-8'))
        team_list = []
        for team in response["result"]["teams"]:
            team_list.append(team["fq_name"])
        user_metadata["teams"] = team_list
        return user_metadata

    def export_team_user_metadata(self, team_name, json_file):
        member_list = self.get_team_memberships(team_name)
        members = {}
        for member in member_list:
            members[member] = self.get_user_metadata(member)
            members[member]["teams"] = team_list
        with open(json_file, 'w') as fp:
            json.dump(members, fp)
        return members

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
            result_msgs = self.get_team_chat_channel(keybase_team, topic)
            result_msgs["result"]["messages"].reverse()
            mah_messages["topic_name"][topic] = result_msgs

        text_file = open(output_file, "w")
        n = text_file.write(json.dumps(mah_messages))
        text_file.close()


    def get_root_messages(self, mah_messages, db):
        for topic in mah_messages["topic_name"]:
            for message in mah_messages["topic_name"][topic]["result"]["messages"]:
                if message["msg"]["content"]["type"] == "headline":
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "headline",
                        txt_body =  message["msg"]["content"]["headline"]["headline"],
                        from_user = message["msg"]["sender"]["username"],
                        sent_time = message["msg"]["sent_at"],
                        ))
                elif message["msg"]["content"]["type"] == "join":
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "join",
                        from_user = message["msg"]["sender"]["username"],
                        sent_time = message["msg"]["sent_at"],
                        ))
                elif message["msg"]["content"]["type"] == "metadata":
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "metadata",
                        from_user = message["msg"]["sender"]["username"],
                        txt_body =  json.dumps(message["msg"]["content"]["metadata"]),
                        sent_time = message["msg"]["sent_at"]
                        ))
                elif message["msg"]["content"]["type"] == "attachment":
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "attachment",
                        from_user = message["msg"]["sender"]["username"],
                        txt_body =  json.dumps(message["msg"]["content"]["attachment"]),
                        sent_time = message["msg"]["sent_at"]
                        ))
                elif message["msg"]["content"]["type"] == "unfurl":
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "unfurl",
                        from_user = message["msg"]["sender"]["username"],
                        txt_body =  json.dumps(message["msg"]["content"]["unfurl"]),
                        sent_time = message["msg"]["sent_at"]
                        ))
                elif message["msg"]["content"]["type"] == "system":
                    if "at_mention_usernames" in message["msg"]:
                        at_mention_usernames = json.dumps(message["msg"]["at_mention_usernames"])
                    else:
                        at_mention_usernames = None
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "system",
                        from_user = message["msg"]["sender"]["username"],
                        txt_body =  json.dumps(message["msg"]["content"]["system"]),
                        sent_time = message["msg"]["sent_at"],
                        userMentions = at_mention_usernames
                        ))
                elif message["msg"]["content"]["type"] == "leave":
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "leave",
                        from_user = message["msg"]["sender"]["username"],
                        sent_time = message["msg"]["sent_at"],
                        ))
                elif message["msg"]["content"]["type"] == "delete":
                    db.session.add( Messages( 
                        team = "complexityweekend.oct2020", 
                        topic = topic,
                        msg_id = message["msg"]["id"],
                        msg_type = "delete",
                        from_user = message["msg"]["sender"]["username"],
                        sent_time = message["msg"]["sent_at"],
                        msg_reference = message["msg"]["content"]["delete"]["messageIDs"][0]
                        ))
                elif message["msg"]["content"]["type"] == "text":
                    urls = self.extractor.find_urls(message["msg"]["content"]["text"]["body"])
                    if len(urls) == 0:
                        db.session.add( Messages( 
                            team = "complexityweekend.oct2020", 
                            topic = topic,
                            msg_id = message["msg"]["id"],
                            msg_type = "text",
                            from_user = message["msg"]["sender"]["username"],
                            sent_time = message["msg"]["sent_at"],
                            txt_body =  message["msg"]["content"]["text"]["body"],
                            word_count = len(message["msg"]["content"]["text"]["body"].split(" ")),
                            userMentions = json.dumps(message["msg"]["content"]["text"]["userMentions"])
                            ))
                    else:
                        db.session.add( Messages( 
                            team = "complexityweekend.oct2020", 
                            topic = topic,
                            msg_id = message["msg"]["id"],
                            msg_type = "text",
                            from_user = message["msg"]["sender"]["username"],
                            sent_time = message["msg"]["sent_at"],
                            txt_body =  message["msg"]["content"]["text"]["body"],
                            urls = json.dumps(urls),
                            num_urls = len(urls),
                            word_count = len(message["msg"]["content"]["text"]["body"].split(" ")),
                            userMentions = json.dumps(message["msg"]["content"]["text"]["userMentions"])
                            ))
        db.session.commit()
    
    def get_reaction_messages(self, mah_messages, db):
        for topic in mah_messages["topic_name"]:
            for message in mah_messages["topic_name"][topic]["result"]["messages"]:
                if message["msg"]["content"]["type"] == "reaction":
                    root_msg_id = message["msg"]["content"]["reaction"]["m"]
                    root_msg = db.session.query(Messages).filter_by(topic=topic).filter_by(msg_id = root_msg_id)
                    if root_msg.count() == 1:
                        db.session.add( Messages( 
                            team = "complexityweekend.oct2020", 
                            topic = topic,
                            msg_id = message["msg"]["id"],
                            msg_type = "reaction",
                            from_user = message["msg"]["sender"]["username"],
                            sent_time = message["msg"]["sent_at"],
                            reaction_body =  message["msg"]["content"]["reaction"]["b"],
                            msg_reference = root_msg.first().id
                        ))
                if message["msg"]["content"]["type"] == "edit":
                    root_msg_id = message["msg"]["content"]["edit"]["messageID"]
                    root_msg = db.session.query(Messages).filter_by(topic=topic).filter_by(msg_id = root_msg_id)
                    if root_msg.count() == 1:
                        db.session.add( Messages( 
                            team = "complexityweekend.oct2020", 
                            topic = topic,
                            msg_id = message["msg"]["id"],
                            msg_type = "edit",
                            txt_body =  message["msg"]["content"]["edit"]["body"],
                            from_user = message["msg"]["sender"]["username"],
                            sent_time = message["msg"]["sent_at"],
                            msg_reference = root_msg.first().id
                        ))
        db.session.commit()
        
    def convert_json_to_sql(self, json_file, sql_connection_string):
        db = DB(sql_connection_string)
        mah_messages = json.load(open(json_file, 'r'))
        self.get_root_messages(mah_messages,db)
        self.get_reaction_messages(mah_messages, db)
        print("Conversion from json to sql complete")

    def export_text_msgs_to_csv(self, sql_connection_string, output_file):
        db = DB(sql_connection_string)
        mah_messages = db.session.query(Messages).filter_by(msg_type = "text")
        msg_list = [["text_messages"]]
        for message in mah_messages:
            msg_list.append([str(message.txt_body)])
        import csv
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(msg_list)

    def message_table_to_csv(self, table_object, sql_connection_string, csv_file_name):
        db = DB(sql_connection_string)
        mah_columns = []
        for column in table_object.__table__.c:
            mah_columns.append(str(column).split(".")[1])
        import csv
        with open(csv_file_name, 'w') as f:
            out = csv.writer(f)
            for row in db.session.query(table_object).all():
                full_row = []
                for column_name in mah_columns:
                    full_row.append(row.__dict__[column_name])
                out.writerow(full_row)
