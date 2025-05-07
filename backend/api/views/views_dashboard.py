# Standard library imports
import json
import datetime

#Local application imports
from api.models import Events, Events_scheduled,Events_available



class events_handling:
    def __init__(self):
        self.month = datetime.datetime.now().month
        self.year = datetime.datetime.now().year
        
    def obtain_current_sign_ups(self):
        """Filters the database and counts how many people signed up for events the current month"""
        query = Events_scheduled.objects.filter(date_scheduled__month=self.month).count()
        return query
    
    def obtain_no_events_scheduled_for_the_month(self):
        """Filters the database and counts how many events are scheduled for the month"""
        query = Events_available.objects.filter(event_date__month=self.month).count()
        return query
    
    def obtain_events_scheduled_for_the_month(self):
        """Filters the database and obtains the events for the month"""
        table_info = []
        query = Events_available.objects.filter(event_date__month=self.month)
        for events in query:
            table_info.append([events.event_date, events.event.title])
        return table_info
    
    def obtain_signUps_per_month(self):
        """Filters the database and counts how many people signed up for events every month"""
        signUps_per_month = []
        for i in range(1,13):
            query = Events_scheduled.objects.filter(date_scheduled__month=i, date_scheduled__year=self.year).count()
            signUps_per_month.append(query)
        return signUps_per_month
    
    def obtain_SignUps_per_event(self):
        """Filters the database and counts how many people signed up for each event"""
        signUps_per_event = {
            "labels": [],
            "data": []
        }
        events = Events.objects.values('title').distinct()
        
        for e in events:
            signUps_per_event["labels"].append(e["title"])
            query = Events_scheduled.objects.filter(event__event__title=e['title']).count()
            
            signUps_per_event["data"].append(query)
        return signUps_per_event

#Creates an instance of the events_handling class
event = events_handling()

def obtain_top_cards_data(context):
    """Defines the data for the top cards of the dashboard"""
    #Get the monthly sign ups
    monthly_scheduled_events = event.obtain_current_sign_ups()
    
    #Get the number of events scheduled for the month
    monthly_events = event.obtain_no_events_scheduled_for_the_month()
    
    #Adds variables to the context dictionary
    context.update({
        "monthly_scheduled_events":[{ 
                                               "title": "Monthly Sign Ups",
                                               "data": monthly_scheduled_events,
        },
        {
            "title": "Events This Month",
            "data": monthly_events,
        },{
            "title": "Total Sign Ups",
            "data": Events_scheduled.objects.all().count()
        }]
    })
     
    return context


def fetch_line_chart_1_data():
    "Filters the data per month and adds it to the context dictionary"
    signUps_per_month = event.obtain_signUps_per_month()
    data = {
        
            "label": "Sign Ups Per Month",
             "chart" : json.dumps({
            "labels": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "datasets": [{
                "data": signUps_per_month,
            }]})
    
    }
    return data
    
def fetch_line_chart_2_data():
    "Filters the data per event and adds it to the context dictionary"
    signUps_per_event = event.obtain_SignUps_per_event()
    data = {
           
            "label": "Sign Ups Per Event",
            "chart" : json.dumps({
            "labels": signUps_per_event["labels"],
            "datasets": [{
                "data": signUps_per_event["data"],
            }]})
    
    }
    return data

def fetch_line_charts_data(context):
    chart_1 = fetch_line_chart_1_data()
    chart_2 = fetch_line_chart_2_data()
    context.update({"line_charts": [chart_1, chart_2]})
    return context

def create_monthly_events_table(context):
    events = event.obtain_events_scheduled_for_the_month()
    context.update({"event_table": 
                    {
                        "headers": ["Event Date", "Event Name"],
                        "rows": events
                    }
    })
    return context

def dashboard_callback(request, context):
    """Adds the data to the context dictionary for the dashboard"""
    obtain_top_cards_data(context)
    fetch_line_charts_data(context)
    create_monthly_events_table(context)
    return context
