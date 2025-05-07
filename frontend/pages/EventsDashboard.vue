<script setup>
  import { ref, shallowRef,  onMounted } from "vue";
  import { useEventStore } from "@/stores/event.js";
  import { useUserStore } from "@/stores/user.js";
  import Fuse from 'fuse.js';
  import EventInfoPopUp from "@/components/ui/EventInfoPopUp.vue";
  import PopUp from "~/components/ui/PopUp.vue";
  import WarningPopup from "~/components/ui/WarningPopup.vue";
  import CreateEvent from "~/components/ui/CreateEvent.vue";
  import ConfirmationPopup from "~/components/ui/ConfirmationPopup.vue";
  import ScheduledEventInfo from "~/components/ui/ScheduledEventInfo.vue";
  

  const eventStore = useEventStore()
  const userStore = useUserStore()

  const currentUser = ref({})
  const userRole = ref('')
  const toast = useToast()
  // First method to be executed
  onBeforeMount(() => {
   
  
   if (userStore.users.firstName == undefined) {
     // Redirect to login page if user is not logged in
     navigateTo('/login')
   }
 });
  onMounted( () => {
    
    eventList.value = eventStore.events // Fetch events from Pinia store
    searchedEvents.value = eventList.value
    selectedEventPopup.value = null
    currentUser.value = userStore.getCurrentUser()
    userRole.value = currentUser.value.role
    
    document.documentElement.classList.remove('dark');
    getUserEvents()
    
    
  });
 
  const warningPopup = ref({
    title: "Title",
    message: "This is the message",
  });

  const items = [
    {
      slot: "calendar",
      label: "Calendar",
      icon: "i-heroicons-calendar",
    },
    {
      slot: "event-list",
      label: "Events",
      icon: "i-heroicons-clipboard",
    },
    {
      slot: "my-events",
      label: "My events",
      icon: "i-heroicons-document",
    },
  ];


  const selectedEventPopup = ref({});
  const selectedScheduledEventPopup = ref({});
  const eventList = ref([]);
  const searchedEvents = ref([]);
  const myEvents = ref([]);
  const submittedEvent = ref({});
  const searchQuery = shallowRef('');
  
  const isFormVisible = ref(false);
  const isCreateEventVisible = ref(false);
  const isCreateConfirmVisible = ref(false);
  const isEventInfoVisible = ref(false);
  const isScheduledEventsVisible = ref(false);
  const deleteEventConfirm = ref(false);
  const evtPopupConfirm = ref(false);
  const isWarningPopupActive = ref(false);

  function getUserEvents() {
    myEvents.value = Array.isArray(userStore.getScheduledEvents()) 
      ? userStore.getScheduledEvents() 
      : [userStore.getScheduledEvents()];
  }

  const closePopupByType = (popup = "normal") => {
    const visibilityMap = {
      schedule: () => (isFormVisible.value = false),
      normal: () => (isCreateEventVisible.value = false),
      eventInfo: () => (isEventInfoVisible.value = false),
      eventInfoConfirm: () => (evtPopupConfirm.value = false),
      warning: () => (isWarningPopupActive.value = false),
      createConfirmation: () => (isCreateConfirmVisible.value = false),
      scheduledEvents: () => (isScheduledEventsVisible.value = false),
      deleteEventConfirm: () => (deleteEventConfirm.value = false),
    };

    visibilityMap[popup]?.();
  };

   

  const openPopupByType = (popup = "normal") => {
    const visibilityMap = {
      schedule: () => (isFormVisible.value = true),
      normal: () => (isCreateEventVisible.value = true),
      eventInfo: () => (isEventInfoVisible.value = true),
      eventInfoConfirm: () => (evtPopupConfirm.value = true),
      warning: () => (isWarningPopupActive.value = true),
      createConfirmation: () => (isCreateConfirmVisible.value = true),
      scheduledEvents: () => (isScheduledEventsVisible.value = true),
      deleteEventConfirm: () => (deleteEventConfirm.value = true),
    };

 

    visibilityMap[popup]?.();
  };
 
  const generateRandomId = () => {
    const min = 100000;
    const max = 999999;
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  const handleIdFromCurrentCardSelection = (e_id, clickedDate)=>{
    const selectedEvent = eventStore.getEventByIdAndDate(e_id, clickedDate);
    if (selectedEvent) {
      selectedEventPopup.value = selectedEvent; // Assign selected event
      openPopupByType('eventInfo');
    }
  }

  const handleScheduledEventCard = (e_id, clickedDate)=>{
    const selectedEvent = eventStore.getEventByIdAndDate(e_id, clickedDate);
    if (selectedEvent) {
      selectedScheduledEventPopup.value = selectedEvent; // Assign selected event
      openPopupByType('scheduledEvents');
    }
  }

  const scheduleEvent = (event) => {
    // check if capacity is available
    if (event.spaces_available <= 0) {
      closePopupByType('eventInfoConfirm')
      closePopupByType('eventInfo')
      handleWarning('Warning', 'Capacity is not available')
      return
    }
    const events =  userStore.getScheduledEvents()
    const event_ = eventStore.getEventById(event.date_id)
 
    if ( event_ in events) {
      closePopupByType('eventInfoConfirm')
      closePopupByType('eventInfo')
      handleWarning('Warning', 'This event is already scheduled')
      return
    }
    

   
    userStore.addScheduledEvent(event.id, event.dateId)
    myEvents.value.push(event)
    
  
    // Update current user
    currentUser.value = userStore.getCurrentUser()
    toast.add({ title: event.title+' has been scheduled!' })
    
    // Decrease capacity of the event
    eventStore.decreaseCapacity(event.id)
    // closing popups
    closePopupByType('eventInfoConfirm')
    closePopupByType('eventInfo')
  }

  const getEventsFromDates = (evtObj, dates) => {
    const events = []
    dates.forEach(date => {
      // Clone the object to avoid modifying the original evtObj
      const newEvent = {...evtObj}
      newEvent.startDate = date
      events.push(newEvent)
    });
    return events
  }

  const createEvent = () => {
    if (!submittedEvent.value) return
    // If event has more than one date
    if (submittedEvent.value.dates.length > 0) {
      getEventsFromDates(submittedEvent.value, submittedEvent.value.dates).forEach(evt => {
        evt.dateId = handleSameIdIssue(eventStore.getAllDateIds())
        eventStore.addEvent(evt)
      })
      closePopupByType('schedule')
      closePopupByType('createConfirmation')
      toast.add({ title: submittedEvent.value.title+' has been created!' })
      return
    }

  
    closePopupByType('schedule')
    closePopupByType('createConfirmation')
    toast.add({ title: submittedEvent.value.title+' has been created!' })
    eventStore.addEvent(submittedEvent.value)
  }

  const handlingAddClass = (formData) => {

    formData.id = handleSameIdIssue(eventStore.getAllEventIds())

    formData.time = formData.time
    formData.timezone = eventStore.getTimeZone()
    submittedEvent.value = formData
    // eventStore.addEvent(formData)

    // Opening the confirmation popup
    openPopupByType('createConfirmation')


    // closePopupByType('schedule');
  }

  const handleWarning = (title, message) => {
    warningPopup.value.title = title;
    warningPopup.value.message = message;
    openPopupByType('warning');
  }

  const handleSameIdIssue = ( ids) => {
    const newId = ref(generateRandomId());

    do {
      newId.value = generateRandomId();
    } while (ids.some(e_id => e_id === newId.value));

    return newId.value
  }

  const handleCreateEventBtn = () => {
    openPopupByType('schedule')
  }

  const deleteEventFromUser = () => {
    const event_ = eventStore.getEventById(selectedScheduledEventPopup.value.id)
    userStore.removeScheduledEvent(event_.id, event_.dateId)
    myEvents.value = myEvents.value.filter(e => e.id !== selectedScheduledEventPopup.value.id)
    closePopupByType('deleteEventConfirm')
    closePopupByType('scheduledEvents')
    toast.add({ title: selectedScheduledEventPopup.value.title+' has been deleted!' })
  }

  const handleSearch = () => {
    if (searchQuery.value === '') {
      searchedEvents.value = eventList.value
    }
    const fuse = new Fuse(eventList.value, {
      keys: ["title"], // Search by event name
      threshold: 0.3, // Lower value = stricter matching
    });
    const results = fuse.search(searchQuery.value);
    searchedEvents.value = results.map(result => result.item);
  }


</script>
<template>
    <Header/>
    <WarningPopup
      v-if="isWarningPopupActive"
      name="warning-popup"
      class="z-[70]"
      :title="warningPopup.title"
      :message="warningPopup.message"
      @confirm="closePopupByType('warning')"
      confirmText="Ok"
    />
    <ConfirmationPopup
      v-if="deleteEventConfirm"
      title="Delete Event"
      message="Are you sure you want to delete this event?"
      confirmText="Yes"
      cancelText="No"
      class="z-[70]"
      @close="closePopupByType('deleteEventConfirm')"
      @confirm="deleteEventFromUser(selectedEventPopup)"

    />

    <ConfirmationPopup
      v-if="isCreateConfirmVisible"
      title=""
      message="Are you sure you want to proceed?"
      confirmText="Yes"
      cancelText="No"
      class="z-[70]"
      @close="closePopupByType('createConfirmation')"
      @confirm="createEvent"

    />

    <PopUp
      name="schedule-event-confirmation-popup"
      class="z-[70]"
      :show="evtPopupConfirm"
      title="Confirmation"
      message="Are you sure you want to proceed?"
      confirmText="Yes"
      cancelText="No"
      :exitBtn="false"
      @close="closePopupByType('eventInfoConfirm')"
      @confirm="scheduleEvent(selectedEventPopup)"
    />
    <!-- Form Popup -->
    <transition name="fade">
      <PopUp
        :show="isFormVisible"
        title=""
        message=""
        :exitBtn="false"
        class="z-[10]"
      >
        <template #additional-content>
          <CreateEvent 
            @create-class="handlingAddClass" 
            @close="closePopupByType('schedule')" 
            class="w-1/4"
            @warningPopUp = "handleWarning"
          />
        </template>
      </PopUp>
    </transition>
    
    <!-- My events view -->
    <transition name="fade">
      <ScheduledEventInfo 
        v-if="isScheduledEventsVisible"
        class="z-[60]"
        :eventObj="selectedScheduledEventPopup"
        confirmText="Delete"
        cancelText="Close"
        @close="closePopupByType('scheduledEvents')"
        @confirm="openPopupByType('deleteEventConfirm')"
        />
    </transition>
    <!-- Event information pop up -->
    <transition name="fade">
      <EventInfoPopUp 
        v-if="isEventInfoVisible"
        class="z-[60]"
        :eventObj="selectedEventPopup"
        confirmText="Schedule"
        cancelText="Close"
        @close="closePopupByType('eventInfo')"
        @confirm="openPopupByType('eventInfoConfirm')"
        />
    </transition>
    <!-- Tabs (Calendar & event list) -->
    <UTabs :items="items" class="flex flex-col bg-white text-black">
      <template #calendar="{ item }">
        <CreateEventBtn v-if="userRole === 'admin'" @button-clicked="handleCreateEventBtn"/>
        <Calendar class="mb-[-10rem] mt-[-2rem]" :eventList="eventList" @close-popup="closePopupByType" @event_id="handleIdFromCurrentCardSelection" @new_event_trigger="handleCreateEventBtn"/>
      </template>

      <template #event-list="{ item }">
        <div name="event-list" class="flex flex-col items-center pt-10 gap-12 mb-20">
          <!-- <UInput v-model="searchTerm" @change="handleSearch" class="w-1/3" icon="i-lucide-search" size="lg" variant="outline" placeholder="Search..." /> -->
          <Card v-for="event in searchedEvents" :key="event.id" :cardObj="event" @event_id="handleIdFromCurrentCardSelection"/>
        </div>
      </template>
      <template #my-events="{ item }">
        <div name="my-events" class="flex flex-col items-center pt-10 gap-12 mb-20  min-h-screen">
          <Card v-for="event in myEvents" :key="event.id" :cardObj="event" @event_id="handleScheduledEventCard"/>
          <div v-if="myEvents.length === 0" class="flex flex-col items-center pt-10 mt-20 gap-4">
            <img src="@/assets/images/check-box-empty.png" alt="check_box_empty" class="h-6 w-6 opacity-40">
            <span class="opacity-40 text-lg">No events scheduled</span>
          </div>
        </div>
      </template>
    </UTabs>
    <UNotifications color="rose"/>
    <Footer></Footer>
</template>