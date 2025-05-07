import { defineStore } from 'pinia';


export const useEventStore = defineStore('eventStore', {
  state: () => ({
    events: [], // Initialize state with JSON data
    dates: [], // Initialize state with JSON data
  }),
  actions: {
    // This function takes event.JSON and dates.JSON and includes dates into events based on their ID's
    // Instead of the JSON, retrieve data from a database
    // Function called in EventsDashboard.vue onMounted
    // Events will have a date id to identify different events
   
    async getDates(){
      const api = "http://localhost:8000/api/Add_event_date";
      const api_2 = "http://localhost:8000/api/events";
    
      try {

        //Rewrite this code into your ugly way
        // First request
        const datesResponse = await $fetch(api, { method: "GET" });
        this.dates = datesResponse;
    
        // Second request, depends on the first one
        const eventsResponse = await $fetch(api_2, { method: "GET" });
        this.events = eventsResponse;
       
        // Initialize store after fetching both sets of data
        console.log(toRaw(this.dates))
        this.initializeStore();
        console.log(toRaw(this.events))
        console.log(toRaw(this.dates))
        return Promise.resolve();
      } catch (error) {
        console.error("Error fetching dates or events:", error);
      }
    },
    initializeStore() {
      
      this.events = this.events.flatMap(event => {
        // Find all dates matching the event's IDs
        const eventDates = this.dates
          .filter(date => date.event === event.id)
          .map(date => ({id: date.id, date: date.event_date })); // Extract only the date string
        

        // If no dates exist, keep the original event with its startDate
        if (eventDates.length === 0) {
          // continue
          return { ...event, startDate: null };
        }
    
        // Otherwise, duplicate event for each date
        return eventDates.map(date => ({
          ...event,       // Copy event properties
          startDate: date.date, // Replace startDate with each event-specific date
          dateId: date.id
        }));
      });
    
    },
    async addEvent(newEvent) {
      // newEvent {id,title,startDate, dates[],time,duration,instructor,category,description,capacity,imageUrl}
      // Add the new event with not date id
      // Add this event to the db
      console.log(newEvent["dates"])
      //Let's start by checking if the event exists in the database
      await $fetch("http://localhost:8000/api/events",{
        method: "POST",
        headers:{
          "Content-Type": "application/json"
        },
        body:{
          
            "title": newEvent["title"],
            "description": newEvent["description"],
            "time_of_event": newEvent["time"]+":00",  
            "spaces_available":newEvent["capacity"] , 
            "image_link": newEvent["imageUrl"],
            "category": newEvent["category"],
            "duration": newEvent["duration"],
            "instructor": newEvent["instructor"],
            "dates": newEvent["dates"]
            
        }
      })
      this.events.push(newEvent);
    },
   
   
    decreaseCapacity(eventId) {
      const event = this.events.find(event => event.id === eventId);
      if (event) {
        event.spaces_available--;
      }
    },
    increaseCapacity(eventId) {
      const event = this.events.find(event => event.id === eventId);
      if (event) {
        event.spaces_available++;
      }
    },
    getEventById(eventId) {
      return this.events.find(event => event.id === eventId  );
    },
    getEventByIdAndDate(eventId , date) {
      return this.events.find(event => event.id === eventId && event.startDate === date);
    },
    getAllEventIds() {
      return this.events.map(event => event.id);
    },
    getAllDateIds() {
      return this.dates.map(date => date.id);
    },
    //No entiendo
    getEventByDateId(dateId) {
     
      dateId = parseInt(dateId)
      return this.events.find(event =>  event.dateId === dateId);
    },
  
    getTimeZone() {
      const timeZoneAbbreviations = {
        "America/New_York": "EST",
        "America/Chicago": "CST",
        "America/Denver": "MST",
        "America/Los_Angeles": "PST",
      };
      // Get the user's timezone
      const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      // Convert to abbreviation
      const userTimeZoneAbbr = timeZoneAbbreviations[userTimeZone] || userTimeZone; 
      
      return userTimeZoneAbbr;
    },
    translateTimezoneFromAbreviation(timezone){
      // switch case translating from abreviation to timezone
      switch (timezone) {
        case 'EST':
          return 'Eastern Standard';
        case 'CST':
          return 'Central Standard';
        case 'MST':
          return 'Mountain Standard';
        case 'PST':
          return 'Pacific Standard';
        case 'AKST':
          return 'Alaska Standard';
        default:
          return timezone;
      }
    },
    translateTimezoneToAbreviation(timezone){
      // switch case translating from abreviation to timezone
      switch (timezone) {
        case 'Eastern Standard':
          return 'EST';
        case 'Central Standard':
          return 'CST';
        case 'Mountain Standard':
          return 'MST';
        case 'Pacific Standard':
          return 'PST';
        case 'Alaska Standard':
          return 'AKST';
        default:
          return timezone;
      }
    },
    convertingTime24to12(time) {
      if(time!=undefined || time !=null){
      const [hours, minutes] = time.split(':');
      const ampm = hours >= 12 ? 'PM' : 'AM';
      const formattedHours = hours % 12 || 12;
      return `${formattedHours}:${minutes} ${ampm}`;}
    },
    formatTime(time) {
      console.log("from format time:"+time)
      if(time!=undefined || time !=null){
      return this.convertingTime24to12(time)
      }
    },
    formatDateWithSuffix(date){
      // Parse the input date
      if (!date){
        return;
      }
      const newDate = new Date(date.split('-')[0], date.split('-')[1] - 1, date.split('-')[2]);
  
      // Create a new date object adjusted for the specified time zone
      // ... MISING CODE ...
      
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      const formattedDate = new Intl.DateTimeFormat('en-US', options).format(newDate);
      
      const day = newDate.getDate(); // Get the day in the adjusted time zone
      let suffix = 'th';
  
      // Handle suffix for dates
      if (day % 10 === 1 && day !== 11) {
        suffix = 'st';
      } else if (day % 10 === 2 && day !== 12) {
        suffix = 'nd';
      } else if (day % 10 === 3 && day !== 13) {
        suffix = 'rd';
      }
  
      // Return formatted date with suffix
      return formattedDate.replace(/\d+/, day + suffix);
    }
    
  },
});
