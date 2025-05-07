from django.test import TestCase
from .models import Events_scheduled, Events, Events_available
from django.contrib.auth.models import User
# Create your tests here.
import datetime
from .views.views_dashboard import events_handling

#To test views
from django.urls import reverse

d= datetime.timedelta(hours=1)
d_= datetime.date.today()
#Testing the queries for the dashboard
class test_events_handling_class(TestCase):
    #Tests for the events_handling class
    def setUp(self):
        self.event_obj = events_handling()
        #Set this to a month for testing purposes
        self.event_obj.month = 9
        
        #set this to a year for testing purposes
        self.event_obj.year = 2021
        
        #creates an event for testing purposes
        self.user = User.objects.create_user(username="test",password="test")
        self.event = Events.objects.create(title="test",description="test",time_of_event="12:00:00",spaces_available=10,duration=d,image_link="test",category="Art",instructor=self.user)
        self.events_added_for_testing = []
        #Generates a number of events for the month
        self.number_of_events = 4
        for day in range(1,self.number_of_events+1):
            Events_available.objects.create(event=self.event,event_date=f"{self.event_obj.year}-{self.event_obj.month}-{day}")
            self.events_added_for_testing.append( [datetime.date(self.event_obj.year,self.event_obj.month,day),self.event.title])
        
        #Generates a number of sign ups for the month
        self.number_of_sign_ups = 6
        for sign_up in range(self.number_of_sign_ups):
            user_ = User.objects.create_user(username=str(sign_up),password=str(sign_up))
            Events_scheduled.objects.create(event=Events_available.objects.order_by('?').first(),user=user_)
    
    def tearDown(self):
        self.user.delete()
        self.event.delete()  
        Events_available.objects.all().filter(event_date__year=2021).delete()  
        Events_scheduled.objects.all().filter(date_scheduled=d_).delete()
        
    def test_obtain_no_events_scheduled_for_the_month(self):
        """Tests that the function returns the correct number of events scheduled for the month"""
        self.assertEqual(self.event_obj.obtain_no_events_scheduled_for_the_month(),self.number_of_events)
        self.assertNotEqual(self.event_obj.obtain_no_events_scheduled_for_the_month(),0)
    
    def test_obtain_events_scheduled_for_the_month(self):
       """Test that the function returns the right list of events"""
       self.assertEqual(self.event_obj.obtain_events_scheduled_for_the_month(),self.events_added_for_testing)
       self.assertNotEqual(self.event_obj.obtain_events_scheduled_for_the_month(), [])
       
       
    def test_obtain_current_sign_ups(self):
        """Tests that the function returns the correct number of sign ups for the month"""
        self.event_obj.month = datetime.date.today().month
        self.assertEqual(self.event_obj.obtain_current_sign_ups(),self.number_of_sign_ups)
        self.assertNotEqual(self.event_obj.obtain_current_sign_ups(),0)
        
    
    


#Tests for the Events_scheduled model
class Events_scheduledTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",password="test")
        self.event = Events.objects.create(title="test",description="test",time_of_event="12:00:00",spaces_available=10,duration=d,image_link="test",category="Art",instructor=self.user)
        self.event_date = Events_available.objects.create(event=self.event,event_date="2020-06-01")
        self.sign_up = Events_scheduled.objects.create(event=self.event_date,user=self.user)
        self.sign_up.save()
        self.sign_up = Events_scheduled.objects.create(event=self.event_date,user=self.user)
    def tearDown(self):
        self.user.delete()  
        self.event.delete()  
        self.event_date.delete()  
        self.sign_up.delete()
    def test_same_user_sign_up(self):
        """Tests that a user cannot sign up for the same event twice"""
        with self.assertRaises(Exception):
                        self.sign_up.save()
      