from modules.KeybaseAnalytics import KeybaseAnalytics
from database import DB, Messages
class UserAnalytics(KeybaseAnalytics):
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
    
    
    def get_all_links_from_user(self, user):
        user_links = self.db.session.query(Messages).filter(Messages.from_user == user).filter(Messages.num_urls != None)
        return user_links