<template>
  <div class="flex flex-col min-h-screen">
    <!-- Calendar -->
    <div class="flex carousel w-2/3 justify-center items-center mx-auto" :draggable="false" @dragstart.prevent>
      <!-- Calendar Popup -->
      <!-- Calendar -->
      <UCarousel
        v-slot="{ item, index }"
        :items="monthNames"
        :ui="{
          item: 'basis-full',
          container: 'pointer-events: none',
        }"  
        :prev-button="{
          color: 'red',
          icon: 'i-heroicons-arrow-left-20-solid',
          class: '-start-12'
        }"
        :next-button="{
          color: 'red',
          icon: 'i-heroicons-arrow-right-20-solid',
          class: '-end-12',
        }"
        arrows
        class="w-full"
      >
        <div 
        class="max-w-md mx-auto p-4 bg-white shadow-md rounded-lg m-10 w-1/2">
        
          <!-- Month Header -->
          <div class="text-2xl font-bold mb-4 ">
            {{ item }} {{ currentYear }}
          </div>
          <!-- Days of the Week -->
          <div class="grid grid-cols-7 text-center font-medium text-gray-600">
            <div v-for="day in weekDays" :key="day" class="py-2">
              {{ day }}
            </div>
          </div>
          <!-- Calendar Days -->
          <div class="grid grid-cols-7">
            <!-- Empty cells before the first day of the month -->
            <div
            v-for="n in firstDayOfMonth(currentYear, index)"
            :key="'empty-' + n"
            class="bg-gray-100 h-12"
            ></div>
            
          <!-- Days of the month -->
            <button
              v-for="day in daysInMonth(currentYear, index)"
              :key="'day-' + day"
              :class="[
                'h-12 flex-1 w-full items-center justify-center border hover:bg-red-100 active:bg-red-100',
                selectedDay === day && selectedMonth === item ? 'bg-red-300 text-white' : 'bg-white'
              ]"
              @click="handleClick(day, item, index)"
              >
              <span name="ping" class="z-[5]" v-if="checkDateEvent(day, index)">
                <span class="animate-ping float-top float-right h-2 w-2 bg-red-300 z-10 rounded-full small-circle mr-1"></span>
                <span class="float-top float-right h-2 w-2 bg-red-300 z-10 rounded-full small-circle mr-1"></span>
              </span>
              {{ day }}
            </button>
            
          </div>
          <div v-if="selectedMonth === item" class="w-full mt-4 bg-white rounded-lg p-4">
            <!-- Events available -->
            <transition name="fade-in">
              <ul v-if="eventsPerClick.length > 0">
                <h3 class="font-semibold mb-2">Classes:</h3>
                <li v-for="event in eventsPerClick" :key="event.id" class="flex flex-row justify-between mb-2">
                  <p @click="displayEvent(event.id , event.startDate)" class="cursor-pointer hover:text-red-400">{{ formatTime(event.time)}} - {{ event.title }} </p>
                </li>
              </ul>
            </transition>
            <transition name="fade-in">
            <!-- No events message -->
              <div v-if="eventsPerClick.length <= 0" class="text-gray-600 flex flex-col justify-center items-center z-[0]">
                <img src="@/assets/images/check-box-empty.png" alt="check_box_empty" class="h-4 w-4 mb-4 opacity-40">
                <p>No classes available</p>
              </div>
            </transition>
          </div>
          
        </div>
      </UCarousel>
      
    </div>
    
  </div>
  
</template>
<script >
  import PopUp from "~/components/ui/PopUp.vue";
  import EventInfoPopUp from "~/components/ui/EventInfoPopUp.vue";
  import CreateEvent from "~/components/ui/CreateEvent.vue";
  import { useEventStore } from "@/stores/event.js";

  export default {
    components: {
      PopUp,
      CreateEvent,
      EventInfoPopUp
    },
    props: {
      eventList: {
        type: Array,
        required: true,
      }
    },
    emits: ['event_id','warning','new_event_trigger'],
    data() {
      const today = new Date();
      const currentMonth = today.getMonth();
      const currentYear = today.getFullYear();
      const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

      return {
        eventStore: useEventStore(),
        currentMonth,
        currentYear,
        selectedDay:"",
        selectedMonth:"",
        event:[],
        isWarningVisible: false,
        warningMessage:'',
        warningTitle: '',
        isCreateEventVisible: false,
        evtPopupConfirm: false,
        isEventInfoVisible: false,
        isFormVisible: false,
        testEvents: null,
        selectedEventPopup: {
          id: 0,
          title: "",
          desc: "",
          instructor: "",
          instructor_email: "",
          date: "",
          time: ""
        },
        monthNames: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ],
        monthMap : {
          'January': 0,
          'February': 1,
          'March': 2,
          'April': 3,
          'May': 4,
          'June': 5,
          'July': 6,
          'August': 7,
          'September': 8,
          'October': 9,
          'November': 10,
          'December': 11
        },
        eventsPerClick: [
          {
            id: 1,
            title: "Event 1",
            desc: "Description 1",
            instructor: "Instructor 1",
            date: "2023-06-01",
            time: "10:00 AM",
          },
        ],
        weekDays: WEEKDAYS,
      };
    },
    methods: {
      daysInMonth(year , month) {
        return new Date(year, month + 1, 0).getDate();
      },
      firstDayOfMonth(year , month) {
        return new Date(year, month, 1).getDay();
      },
      checkDateEvent(day, mIndex){
        // eventDate
        return this.eventList.some(event => {
        
          if (toRaw(event).startDate !=null){
          const [year, month, eventDay] = event.startDate.split('-').map(Number);
          return (
            year === this.currentYear &&
            month - 1 === mIndex &&
            eventDay === day
          );
      }});
      },
      handleClick(day, month, mIndex ) {
        const monthIndex = this.monthNames.indexOf(month); // Get the month index
        if (monthIndex === -1) {
          console.error("Invalid month name:", month);
          return;
        }
        this.selectedDay = day;
        this.selectedMonth = month;
        // Filter events based on the selected date (day, month, year)
        const filteredEvents = this.eventList.filter(event => {
          if(toRaw(event).startDate!=null){
          const [year, month, day] = event.startDate.split('-').map(Number)
          const eventDate = new Date(Date.UTC(year, month - 1, day+1))
          
          
          return (
            eventDate.getFullYear() === this.currentYear &&
            eventDate.getMonth() === mIndex &&
            eventDate.getDate() === this.selectedDay
          )
    }})
        this.eventsPerClick = filteredEvents;
        // Assigns values manually.
        if (filteredEvents.length > 0) {
          this.selectedEventPopup = { ...filteredEvents[0] }
        }
      },
      displayEvent(id , clickedDate) {
        // sends the id of the clicked event
        this.$emit('event_id', id, clickedDate);
      },
      newEventClicked() {
        this.$emit('new_event_trigger');
      },
      formatTime(time) {
        if(time!=undefined || time !=null){
        return this.eventStore.convertingTime24to12(time.split(':')[0])
        }
      }
    },
    created() {
      this.eventStore = useEventStore()
    }
  };
</script>

<style scoped>
</style>

