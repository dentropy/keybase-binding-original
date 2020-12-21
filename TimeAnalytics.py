from GenerateAnalytics import GenerateAnalytics
from database import DB, Messages
from sqlalchemy import func, asc
from datetime import *
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import calmap
# -4 hours for EST

class TimeAnalytics(GenerateAnalytics):
    def __init__(self, db_url):
        """TimeAnalytics class constructor."""
        self.db = DB(db_url)
        
    def messages_per_day_of_week(self, messages):
        """Generate data to graph messages per day of week."""
        week_list = []
        for i in range(7):
            week_list.append(0)
        for item in messages:
            week_list[(item.sent_time - timedelta(hours=-4)).weekday()] += 1
        print(week_list)
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return {
            "type":"Show X Axis",
            "x_label":"Day of Week",
            "y_label":"Num Messages",
            "x_axis":weekdays, 
            "y_axis":week_list, 
            "title": "Messages Per Day of Week"}
 
    def messages_per_day(self, messages):
        """Generate data to graph messages per day of week."""
        message_days = []
        for item in messages:
            message_day = (item.sent_time - timedelta(hours=-4)).timetuple().tm_yday
            if item not in message_days:
                message_days.append(message_day)
            message_days.append((item.sent_time - timedelta(hours=-4)).timetuple().tm_yday)
        days_messages_happened = sorted(np.unique(message_days))
        
        # In case no messages we on a single day
        days_messages_happened = list(range(min(days_messages_happened), max(days_messages_happened)))
        dates_messages_happened = []
        for day in days_messages_happened:
            dates_messages_happened.append( (datetime(2020, 1, 1) + timedelta(day - 1)) )
        messages_on_days = []
        for i in range(len(days_messages_happened)):
            messages_on_days.append(0)
        for message in message_days:
            messages_on_days[(  message - min(days_messages_happened) - 1  )] += 1
        return {
            "type":"Show X Axis",
            "x_label":"Dates",
            "y_label":"Num Messages",
            "x_axis":dates_messages_happened, 
            "y_axis":messages_on_days, 
            "title": "Messages Per Day"}


    # This Method Works
    def hours_vs_day_scatter_plot(self, mah_team_messages):
        y_hours = []
        for item in mah_team_messages:
            y_hours.append((item.sent_time - timedelta(hours=-4)).hour)
        x_days = []
        for item in mah_team_messages:
            x_days.append((item.sent_time - timedelta(hours=-4)).timetuple().tm_yday)
        plt.scatter(x_days, y_hours, s=np.pi*10,alpha=0.5)
        plt.title('Scatter Plot of When Message Sent Comparing Day Number vs Hour')
        plt.xlabel('Day of year')
        plt.ylabel('Hour of day')
        plt.show()
    
    # TODO, Fork library and fix it, Submit Pull Request
    def plot_calendar_heatmap(self, messages):
        # https://pythonhosted.org/calmap/#calmap.yearplot
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html
        # https://beepb00p.xyz/hpi.html
        time_list = []
        for item in messages:
            time_list.append(item.sent_time - timedelta(hours=-4))
        time_list = np.array(time_list)
        # Day Month Year
        all_days = pd.date_range(start='1/1/2020', end='30/12/2020')
        days = np.random.choice(all_days, len(time_list))
        events = pd.Series(np.random.randn(len(days)), index=time_list)
        plt.figure(figsize=(20, 2.3))
        calmap.yearplot(events, year=2020, daylabels='MTWTFSS')
