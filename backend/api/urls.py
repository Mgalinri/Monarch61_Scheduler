from django.urls import path

from .views import views_apis

urlpatterns = [
    path('events', views_apis.event_list.as_view(), name="events"),
    path('Add_event_date', views_apis.events_dates_available.as_view()),
    path('Event_Sign_Up/<int:pk>', views_apis.eventSignUp.as_view()),
    path('sign_up',views_apis.signUp),
    path('obtain_usernames', views_apis.user_info),
    path('obtain_instructors', views_apis.get_instructors),

]