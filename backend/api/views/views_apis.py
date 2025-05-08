# Django imports
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.db.models import Min
from django.db.models.signals import pre_save

# Third party imports
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics,mixins,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


#Local application imports
from api.models import Events, Events_scheduled,Events_available
from api.serializers import EventSerializer,EventsScheduledSerializer,EventsAvailableSerializer


import environ

env = environ.Env()
environ.Env.read_env('.env')

        
class event_list(generics.ListCreateAPIView,mixins.CreateModelMixin):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    
    
    def perform_create(self, request,*args, **kwargs):
       instance = None
       info = request.data
       query = self.queryset.filter(title = info["title"], time_of_event = info["time_of_event"])
      
       if (query.count()==0):
        
            obj = {
                "title" : info["title"],
                "description" : info["description"],
                "time_of_event" : info["time_of_event"],
                "spaces_available" : info["spaces_available"],
                "image_link" : info["image_link"],
                "duration" : info["duration"],
                "instructor": info['instructor'],
                "category" : info["category"],
               }
            serialize = EventSerializer(data=obj)
              # Check if the data is valid
          
            if serialize.is_valid():
                # Save the object using the serializer
                instance = serialize.save()
         
            else:
                # If invalid, raise a validation error
                raise ValidationError(serialize.errors)
       else:
            instance = query[0]
           
       
       for i in info.get('dates'):    
            events_scheduled_query = Events_available.objects.all().filter(event = instance, event_date = i).count()
            if (events_scheduled_query==0):
                    Events_available.objects.create(event = instance, event_date = i)

    ''' Provides only the events with events scheduled'''
       
    def get(self, *args, **kwargs):
        elements = []
    
        Events_scheduled_query = Events_available.objects.values('event_id').annotate(id=Min('id')).order_by('event_id')
       
        for events in Events_scheduled_query:
            events_query = Events.objects.get(pk=events["event_id"])
            to_dict = model_to_dict(events_query)
            
            Events_scheduled_by_users = Events_scheduled.objects.filter(event_id= events['id']).count()
             
            to_dict['spaces_available']= to_dict['spaces_available']-Events_scheduled_by_users
            to_dict['duration']= str(to_dict['duration'])
            to_dict['instructor'] = User.objects.get(pk=to_dict['instructor']).first_name + " " + User.objects.get(pk=to_dict['instructor']).last_name
            elements.append(to_dict)
        return Response(elements)

class events_dates_available(generics.ListCreateAPIView):
    queryset = Events_available.objects.all()
    serializer_class = EventsAvailableSerializer
    
class eventSignUp(generics.ListCreateAPIView,mixins.DestroyModelMixin, mixins.CreateModelMixin):
    queryset = Events_scheduled.objects.all()
    serializer_class = EventsScheduledSerializer
    
    #Find the event based of the user
    def delete(self, request, *args, **kwargs):
        #Get the event based of the user_id and event id
        info = request.data
      
        query = self.queryset.filter(user_id=info["user_id"],event=info["event_id"])
      
        for event in query:
          
            event.delete()
        return Response(status=status.HTTP_201_CREATED)
    def post(self,request, *args, **kwargs):
        info = request.data
        #Check if the user has already signed up for the event
    
        query = self.queryset.filter(user=info["user"],event=info["event"]).count()
        if (query==0):
            obj = {
                "event": info["event"],
                "user": info["user"],
            }
            serialize = EventsScheduledSerializer(data=obj)
            if serialize.is_valid():
                instance = serialize.save()
                return Response(serialize.data, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError(serialize.errors)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#For the user to sign up it uses Django built in add user method
# More on https://docs.djangoproject.com/en/5.1/topics/auth/default/
@api_view(['POST'])
def signUp(request):
    info = request.data
    user = User.objects.create_user(info['username'],info['email'],info['password'])
    user.first_name = info['first_name']
    user.last_name = info['last_name']
    user.save()
    return Response(status=status.HTTP_201_CREATED)
    




"""Sends email to the person that scheduled a class when the event is scheduled"""
@receiver(pre_save, sender=Events_scheduled)
def my_handler(sender, instance, **kwargs):
    # using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
    print(instance.event.event.instructor.email)
    print()
    message = Mail(\
        #instance.event.event.instructor.email
        from_email='mgalindorivera@gmail.com',
        to_emails= 'galindom@jbu.edu',
        subject='Class Scheduled',
        html_content='''
        <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background-color: #f6f9fc;
      margin: 0;
      padding: 0;
    }
    .email-wrapper {
      max-width: 600px;
      margin: auto;
      background: #ffffff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    .email-header {
      background-color: #00aaff;
      color: #ffffff;
      padding: 30px;
      text-align: center;
    }
    .email-header h1 {
      margin: 0;
      font-size: 26px;
    }
    .email-body {
      padding: 30px;
      color: #333333;
      line-height: 1.6;
    }
    .email-body p {
      margin-bottom: 16px;
    }
    .cta-button {
      display: inline-block;
      padding: 12px 24px;
      background-color: #00aaff;
      color: #ffffff;
      text-decoration: none;
      border-radius: 6px;
      font-weight: bold;
    }
    .email-footer {
      text-align: center;
      padding: 20px;
      font-size: 12px;
      color: #999999;
      background-color: #f0f0f0;
    }
  </style>
</head>
<body>
  <div class="email-wrapper">
    <div class="email-header">
      <h1>You're In! 🎉</h1>
    </div>
    <div class="email-body">
      <p>Hi there,</p>
      <p>Thank you for signing up for <strong>'''+instance.event.event.title+'''<strong>!</p>
      <p>We're thrilled to have you on board. Keep an eye on your inbox for event details, schedules, and exclusive updates.</p>
      <p>If you have any questions before the event, feel free to reach out.</p>
      <a href="#" class="cta-button">View Event Details</a>
    </div>
    <div class="email-footer">
      &copy; 2025 Your Company. All rights reserved.
    </div>
  </div>''')
    try:
        # 
        sg = SendGridAPIClient(env("SENDGRID_KEY"))
        response = sg.send(message)
    except Exception as e:
        print("hello")
        

    pass

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_info(request, format=None):
    data = request.headers.get("Authorization")
    #For testing purposes
    #data = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyOTU4MDUwLCJpYXQiOjE3NDI5NTQ0NTAsImp0aSI6ImM0MTU3Mzk1NjMwOTQ1OWFiMjMzNTA5YzUyOTk1N2U3IiwidXNlcl9pZCI6MX0.Gzcw4mQTaHQFn1iATPKG9u21cu_75sWMNlENdJp3Lmw"
    obtain_token = data.split(" ")
    token = obtain_token[1]
    validate = AccessToken(token)["user_id"]
    obtain_events = Events_scheduled.objects.all().filter(user=validate).values("event_id")
    event_list = []
    for events in obtain_events:
        event_list.append(events["event_id"])
    role = "user"
    user_info = User.objects.all().filter(pk=validate)
    if (user_info[0].is_staff==1):
        role = "admin"

    content = {
        'username': user_info[0].username,
        'first_name':user_info[0].first_name,
        'last_name':user_info[0].last_name,
        'email':user_info[0].email,
        'events':event_list,
        'role': role
        
    }
    return Response(content, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_instructors(request, format=None):
    obtain_instructors = User.objects.all().filter(groups__name= 'teachers').values("first_name","last_name","id")
    content =[]
    for instructors in obtain_instructors:
        content.append([[instructors['id']],[instructors["first_name"]+" "+instructors["last_name"]]]),
        
        
    return Response(content, status=status.HTTP_200_OK)