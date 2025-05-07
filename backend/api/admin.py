# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group


# Third party imports
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin


#Local application imports
from api.models import Events, Events_scheduled, Events_available


admin.site.index_template = "admin/index.html"
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
   form = UserChangeForm
   add_form = UserCreationForm
   change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Events)
class EventsAdmin(ModelAdmin):
    #So that it can display specific values from the db in a table
    list_display = ["title","date_created","category"]
    #So that values can be searched through the search bar
    search_fields = ["title","date_created","category"]
 
    pass

@admin.register(Events_scheduled)
class EventsScheduledAdmin(ModelAdmin):
    #So that it can display specific values from the db in a table
    list_display = ["user","event__event__title"]
    #So that values can be searched through the search bar
    search_fields = ["user","event__event__title"]
    pass # Custom dasboard view
admin.site.index_title = 'Dashboard'

@admin.register(Events_available)
class EventsAvailableAdmin(ModelAdmin):
    list_display = ["event__title","event_date"]
    pass

