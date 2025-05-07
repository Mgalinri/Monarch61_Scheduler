import { defineStore } from 'pinia';
import { ref } from 'vue';

import { useEventStore } from "@/stores/event.js";
//Set user store
export const useUserStore = defineStore('userStore', {
  state: () => ({
    users: [], // Initialize state with JSON data
    currentUserId: 1 //Here im hardcoding the current user this will be updated whenever db is connected
  }),
  actions: {
   
    async initializeUserStore(obj){
      const eventStore = useEventStore()
      const eventDates =  await eventStore.getDates();
      
      this.users = {
      "userId": 1,
      "firstName": obj.first_name,
      "lastName": obj.last_name,
      "email": obj.email,
      "role": obj.role,
      "scheduledEvents": obj.events
       }
      console.log(this.users)
       return Promise.resolve();
    },
    async addScheduledEvent(eventId, dateId) {
      const user = this.getCurrentUser()
      console.log(dateId == toRaw(user.scheduledEvents[0]))
      if (user) {
        if (dateId == toRaw(user.scheduledEvents[0])) {
          console.log("Event already scheduled")
        }
        else {
        user.scheduledEvents.push(eventId + "_" + dateId)}
      }
      await $fetch("http://localhost:8000/api/Event_Sign_Up/"+eventId,{
        method: "POST",
        headers:{
          "Content-Type": "application/json"
        },
        body: {
          'user': this.currentUserId,
          'event': dateId,
        }
      })
      console.log("event added to "+ user.firstName)
    },
    async removeScheduledEvent(eventId, dateId) {

      await $fetch("http://localhost:8000/api/Event_Sign_Up/"+ eventId,{
        method: "DELETE",
        headers:{
          "Content-Type": "application/json"
        },
        body: {
          'user_id': this.currentUserId,
          'event_id': dateId,
        }
      }
      )
    
    
      const eventIdentifier = `${eventId}_${dateId}`
      const user = this.getCurrentUser() // Assuming you have a current user object

      if (!user || !user.scheduledEvents) {
        return; // If user or scheduledEvents is undefined, return false
      }
      // Remove the event from the user's scheduled events
      user.scheduledEvents = user.scheduledEvents.filter(event => event !== eventIdentifier);
      
    },
    getUserRole(userId) {
      const user = this.users.find(user => user.userId === userId);
      if (user) {
        return user.role;
      }
      return null;
    },
    getCurrentUser(){
      return this.users;
    },
  
    getScheduledEvents(){

      const user = this.getCurrentUser()
      if (!user || !user?.scheduledEvents) {
        // Get events from the 
        return []
      }

      const ids = user.scheduledEvents
    
      //set variables to default values
      const eventStore = useEventStore()
      const myEvents = ref([])

      ids.forEach(id => {
        
        const event = eventStore.getEventByDateId(id)
        
        if (event) {
          myEvents.value.push(event) // Only push valid events
          
        }
      });
      return myEvents.value

    },
    isUserAdmin() {
      const user = this.getCurrentUser()
      if (user) {
        return user.role === 'admin'
      }
      return false
    },
    
  },
});
