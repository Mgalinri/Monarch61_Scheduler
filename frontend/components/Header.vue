<template>
  <PopUp
    class="z-[70]"
    :show="userView"
    title="Profile"
    message=""
    confirmText="Ok"
    :exitBtn="false"
    @confirm="handleUserView"
  
  >
    <template #additional-content>
      <div class="flex flex-col h-56 w-80">
        <p class="text-black font-bold">{{ currentUser.firstName }} {{ currentUser.lastName }}</p>
        <p class="text-black">{{ currentUser.email }}</p>
        <br>
        <p title="See on 'My events' tab" class="text-black font-bold">Scheduled Events:</p>
        <ul v-if="allUserEvents.length > 0" class="mt-4 overflow-scroll">
          <li v-for="evt in allUserEvents" :key="evt.id" class="flex flex-col">
            <span class="italic">
              {{ evt?.title }}
            </span>
            <span>
              {{ eventStore.formatDateWithSuffix(evt?.startDate) }}
            </span>
            <hr>
          </li>
        </ul>
        <p v-else class="text-black m-auto">No scheduled events</p>

      </div>
    </template>
  </PopUp>
  
  <header :class="{'sticky top-0 bg-white shadow-md': isSticky, 'transition-all duration-500 ease-in-out': true}" 
  class="bg-white text-white font-sans h-22" >
    <nav class="flex items-center justify-between px-6 py-4">
      <!-- Logo -->
      <div class="text-xl font-bold ml-6">
        <router-link to="/" class="btn">
          <button>
            <img src="../assets/images/monarch_logo_bw.png" class="h-12" alt="">
          </button>
        </router-link>
      </div>
      
      <!-- Navigation Links -->
      <ul class="flex items-center space-x-6 text-black mr-6 text-md gap-10">
        <li>
          <!-- <Dropdown v-model="selectedTimezone" @on-change="handleDropdownOption" :options="options" defaultLabel="Select a timezone" :has-icon="false" /> -->
        </li>
        <li>
          <router-link to="/terms-of-service" class="font-medium hover:text-gray-300">
            <a href="#" class="font-medium hover:text-gray-300">Terms and Conditions</a>
          </router-link>
        </li>
        <li>
          <a href="#" class="font-medium hover:text-gray-300">
            <div class="w-12 h-12" @click="handleProfileClick">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M12 14.4C11.0617 14.402 10.1439 14.1254 9.36285 13.6054C8.58183 13.0853 7.97274 12.3451 7.61274 11.4786C7.25274 10.6121 7.15803 9.65817 7.34061 8.73777C7.52318 7.81737 7.97483 6.97186 8.63833 6.30836C9.30183 5.64486 10.1473 5.19321 11.0677 5.01064C11.9881 4.82806 12.942 4.92277 13.8085 5.28277C14.6751 5.64277 15.4153 6.25186 15.9353 7.03288C16.4554 7.8139 16.732 8.7317 16.73 9.67004C16.73 10.9245 16.2317 12.1276 15.3446 13.0147C14.4576 13.9017 13.2545 14.4 12 14.4ZM12 6.40004C11.3588 6.39806 10.7314 6.5864 10.1972 6.94121C9.66311 7.29602 9.24628 7.80134 8.99952 8.3932C8.75275 8.98505 8.68716 9.63682 8.81105 10.266C8.93493 10.8951 9.24272 11.4734 9.69544 11.9275C10.1482 12.3816 10.7255 12.6912 11.3542 12.817C11.983 12.9429 12.635 12.8793 13.2276 12.6344C13.8202 12.3894 14.3268 11.9741 14.6833 11.4411C15.0397 10.9081 15.23 10.2813 15.23 9.64004C15.2221 8.78767 14.8787 7.97275 14.274 7.37189C13.6694 6.77103 12.8524 6.43263 12 6.43004V6.40004Z" fill="#000000"></path> <path d="M19 19.28C18.832 19.2794 18.6691 19.2217 18.5383 19.1163C18.4074 19.0109 18.3163 18.864 18.28 18.7C17.9815 17.4723 17.2788 16.3807 16.2848 15.6008C15.2909 14.8208 14.0634 14.3979 12.8 14.4H11.2C9.93828 14.4001 8.71317 14.8241 7.72124 15.6039C6.72932 16.3836 6.02807 17.474 5.73 18.7C5.70636 18.7958 5.66408 18.8861 5.60555 18.9656C5.54703 19.0452 5.47341 19.1124 5.38891 19.1635C5.30441 19.2145 5.21068 19.2485 5.11306 19.2633C5.01545 19.2781 4.91587 19.2736 4.82 19.25C4.72414 19.2263 4.63387 19.1841 4.55435 19.1255C4.47482 19.067 4.40761 18.9934 4.35654 18.9089C4.30546 18.8244 4.27154 18.7307 4.25669 18.633C4.24184 18.5354 4.24636 18.4358 4.27 18.34C4.64867 16.7879 5.53761 15.408 6.79426 14.4216C8.0509 13.4351 9.60243 12.8993 11.2 12.9H12.79C14.3898 12.8963 15.9442 13.4322 17.2017 14.4212C18.4592 15.4102 19.3465 16.7944 19.72 18.35C19.7655 18.5435 19.7334 18.7471 19.6306 18.9172C19.5278 19.0873 19.3625 19.2103 19.17 19.26L19 19.28Z" fill="#000000"></path> <path d="M12 22.31C9.96088 22.31 7.96755 21.7053 6.27208 20.5725C4.57661 19.4396 3.25515 17.8294 2.47481 15.9455C1.69447 14.0616 1.4903 11.9886 1.88811 9.98863C2.28592 7.98868 3.26786 6.15162 4.70974 4.70974C6.15162 3.26786 7.98868 2.28592 9.98863 1.88811C11.9886 1.4903 14.0616 1.69447 15.9455 2.47481C17.8294 3.25515 19.4396 4.57661 20.5725 6.27208C21.7053 7.96755 22.31 9.96088 22.31 12C22.3074 14.7336 21.2203 17.3544 19.2874 19.2874C17.3544 21.2203 14.7336 22.3074 12 22.31ZM12 3.19001C10.2576 3.19001 8.55423 3.7067 7.10543 4.67476C5.65664 5.64282 4.52744 7.01875 3.86063 8.62857C3.19382 10.2384 3.01935 12.0098 3.35929 13.7188C3.69922 15.4277 4.5383 16.9975 5.7704 18.2296C7.0025 19.4617 8.57229 20.3008 10.2813 20.6407C11.9902 20.9807 13.7616 20.8062 15.3714 20.1394C16.9813 19.4726 18.3572 18.3434 19.3253 16.8946C20.2933 15.4458 20.81 13.7425 20.81 12C20.8074 9.66426 19.8783 7.42494 18.2267 5.77332C16.5751 4.1217 14.3358 3.19265 12 3.19001Z" fill="#000000"></path> </g></svg>
            </div>
          </a>
        </li>
        
      </ul>
    </nav>
  </header>
</template>
  
<script setup>
  import { ref } from 'vue'
  import { onMounted, onBeforeUnmount } from 'vue';
  import { useUserStore } from "@/stores/user.js";
  import PopUp from "~/components/ui/PopUp.vue";
  import { useEventStore } from '~/stores/event';
  
  const userStore = useUserStore()
  const eventStore = useEventStore()
  const currentUser = ref(userStore.getCurrentUser())
  // const options = ref(['Eastern Standard', 'Central Standard', 'Mountain Standard', 'Pacific Standard', 'Alaska Standard']);
  const allUserEvents = ref([])
  const userView =ref(false)
  const isSticky = ref(false);

  onMounted(() => {
      window.addEventListener('scroll', handleScroll);
      currentUser.value = userStore.getCurrentUser();
      allUserEvents.value = userStore.getScheduledEvents()
     
  });
  onBeforeUnmount(() => {
      window.removeEventListener('scroll', handleScroll);
  });
  const handleScroll = () => {
      if (window.scrollY > 0) {
          isSticky.value = true;
      } else {
          isSticky.value = false;
      }
  };
  const handleUserView = () => {
    userView.value = false
  };
  const handleProfileClick = () => {
    userView.value = true
    console.log("helloo")
    allUserEvents.value = userStore.getScheduledEvents() //updating events list per every click
    console.log(allUserEvents.value)
  }
</script>
  
<style scoped>
    div[role="menu"] {
        transition: all 0.2s ease-in-out;
    }
    .sticky {
        position: block;
        top: 0;
        left: 0;
        right: 0;
        width: 100%;
        z-index: 10; /* Ensures the header stays on top */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .sticky + .content {
        padding-top: 70px !important; /* Adjust this value to match the header's height */
    }

    /* Optional: Add transition for smoothness */
    .sticky {
        transition: all 0.3s ease-in-out;
    }
</style>
  