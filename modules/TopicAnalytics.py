from modules.KeybaseAnalytics import KeybaseAnalytics
class TopicAnalytics(KeybaseAnalytics):
    def __init__(self, db_url):
        """GeneratedAnalytics class constructor."""
        self.db = DB(db_url)
        self.user_list = self.get_list_all_users()
        self.topic_list = self.get_list_all_topics()
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
