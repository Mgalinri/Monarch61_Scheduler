#Python Standard Library Imports
import datetime

#Django imports
from django.contrib.auth.models import User
from django.utils.dateparse import parse_duration

#Third Party Imports
from rest_framework import serializers

#Local Application Imports  
from api.models import Events,Events_scheduled, Events_available




class EventSerializer(serializers.ModelSerializer):
   
    dates = serializers.SerializerMethodField()
     
    
    class Meta:
        model = Events
        fields = ["title","description","time_of_event","spaces_available","image_link","category","dates","duration","instructor"]
        read_only_fields = ["id",'date_created']
    
    def to_internal_value(self, data):
        """Handles the duration value"""
        #This was used instead of value, because value obtains the value of the field as 
        #the datatype in the model
      
        print(data["duration"])
      
        if(isinstance(data['duration'], (int,float))):
            data['duration'] = datetime.timedelta(hours=data['duration'],days=0)
        elif(isinstance(data['duration'], str)):
            data['duration'] =  parse_duration(data['duration'])  
        
        inst = inst = User.objects.get(pk=data['instructor'])
        
        return {
            'title': data['title'],
            'description': data['description'],
            'time_of_event': data['time_of_event'],
            'spaces_available': data['spaces_available'],
            'image_link': data['image_link'],
            'category': data['category'],
            'duration': data['duration'],
            'instructor': inst,   
        }
       
    
    def get_dates(self,obj):
        return self.context['request'].data.get('dates')
    
   
   
class EventsScheduledSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events_scheduled
        fields = ["user","event","id"]
        read_only_fields = ['id']

class EventsAvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events_available
        fields = ["event","event_date","id"]
        read_only_fields = ['id']

