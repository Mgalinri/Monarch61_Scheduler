#python standard library imports
import datetime as time_

#django imports
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


d= time_.timedelta(hours=1)



#To hold the events
class Events(models.Model):

    category_choices ={
        "Art": "Art",
        "Community": "Community",
        "Personal Growth": "Personal Growth",
        "Wellness" : "Wellness",
        "Rooted for Teen Girls": "Rooted for Teen Girls",
        "Service" : "Service",
        "Event/Workshop": "Event/Workshop",
        "Trainings" : "Trainings",
    } 
    duration_choices ={
         time_.timedelta(hours=0.5):"0.5 hours",
         time_.timedelta(hours=1):"1 hour",
         time_.timedelta(hours=1.5):"1.5 hours", 
         time_.timedelta(hours=2):"2 hours",
         time_.timedelta(hours=2.5):"2.5 hours",
         time_.timedelta(hours=3):"3 hours",
    }
  
    title = models.CharField(max_length=60,verbose_name="Event")
    description = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    time_of_event = models.TimeField(auto_now=False, auto_now_add=False)
    spaces_available = models.IntegerField(default=0)
    duration = models.DurationField(default=d, choices=duration_choices)
    image_link = models.CharField(max_length=200)
    category = models.CharField(max_length=100,choices=category_choices)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=User.objects.first().id, limit_choices_to={'groups__name': 'teachers'})
    #Handle not creating the same event twice
    def save(self, *args, **kwargs):
            count_=Events.objects.filter(title=self.title,time_of_event=self.time_of_event).count()
            #Django calls save for both insert an update, so we need to check if the pk is None
            #If the pk is None, it means that the object is being created for the first time
            if(count_>=1 and self.pk is None):
                raise Exception("This event has already been created")
            else:
                super(Events, self).save(*args, **kwargs)
    def __str__(self):
        return self.title 

class Events_available(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    event_date = models.DateField(auto_now_add=False)
    #Handle that an event is not scheduled twice on the same date
    def save(self, *args, **kwargs):
            count_=Events_available.objects.filter(event_date=self.event_date, event=self.event).count()
            if(count_>=1 and self.pk is None):
                raise Exception("This event has already been created")
            else:
                super(Events_available, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.event.title 
                
class Events_scheduled(models.Model):
        date_scheduled = models.DateField(auto_now_add=True)
        event= models.ForeignKey(Events_available, on_delete=models.CASCADE)
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        
        def save(self, *args, **kwargs):
            count_=Events_scheduled.objects.filter(user=self.user, event=self.event).count()
             
            #Query number of people signed up for the event and the event available
            people_signed_up=Events_scheduled.objects.filter(event=self.event).count()
            spaces_available = self.event.event.spaces_available 
           
            if(count_>=1 and self.pk is None):
                raise Exception("You have already signed up for this event")
            elif (people_signed_up>=spaces_available):
                raise Exception("There are no more spaces available for this event")
            else:
                super(Events_scheduled, self).save(*args, **kwargs)
                

