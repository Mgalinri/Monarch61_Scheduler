<template>
    <div name="transparent-black-screen" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 text-gray-700">
      <div name="popup" class="bg-white rounded-lg shadow-lg w-1/3 relative w-[50rem]">
        <!-- Popup Content -->

        <img v-if="eventObj.image_link" :src="eventObj.image_link.slice(0,4)==='http' ? eventObj.image_link : '../../uploads/'+eventObj.image_link" fetchpriority="low" class="object-cover h-64 w-full rounded-t-lg" alt="">
        <div v-if="!eventObj.image_link" class="object-cover bg-gray-200 h-64 w-full rounded-t-lg flex items-center justify-center">
          <img src="@/assets/icons/image_icon.svg" class="w-10 h-10 opacity-50" alt="">
        </div>
        <div name="popup-content" class="flex flex-col gap-4 p-6 px-8">

          <div name="top-icons" class="flex flex-row gap-4 justify-between">
            <span class="flex flex-col gap-4">
              <p class="font-semibold w-[30rem] text-2xl overflow-hidden text-ellipsis">{{ eventObj.title }}</p>
              <UBadge v-if="eventObj.spaces_available == 0" color="rose" variant="solid" size="md">Max capacity reached</UBadge>
            </span>
            <div class="flex flex-row gap-4">
              <span name="duration" class="flex flex-row justify-center gap-2 p-0 m-0">
                <img  class="w-5 h-5" src="@/assets/icons/duration_icon.svg" alt="">
                <p>{{ eventObj.duration }} hrs</p>
              </span>
              <span name="capacity" class="flex flex-row justify-center gap-2 p-0 m-0">
                <img  class="w-5 h-5" src="@/assets/icons/multiple_users.svg" alt="">
                <p> {{ eventObj.spaces_available }}</p>
              </span>
            </div>
          </div>
          <p name="description">{{ eventObj.description }}</p>
          <span name="Date" class="flex flex-row justify-start gap-2  p-0 m-0">
            <img  class="w-5 h-5" src="@/assets/icons/calendar_icon.svg" alt="">
            <p>{{ eventStore.formatDateWithSuffix(eventObj?.startDate) }} </p>
          </span>
          <span name="Time" class="flex flex-row justify-start gap-2  p-0 m-0">
            <img  class="w-5 h-5" src="@/assets/icons/time_icon.svg" alt="">
            <p>{{ eventStore.convertingTime24to12(eventObj.time_of_event) }}</p>
          </span>
          <span name="Instructor" class="flex flex-row justify-start gap-2  p-0 m-0">
            <img  class="w-5 h-5" src="@/assets/icons/user_single_icon.svg" alt="">
            <p>{{eventObj.instructor}}</p>
          </span>
          <span name="Category" class="flex flex-row justify-start gap-2  p-0 m-0">
            <img  class="w-5 h-5" src="@/assets/icons/category_icon.svg" alt="">
            <p>{{ eventObj.category }}</p>
          </span>
          <hr>
        </div>
        <!-- Lower Buttons -->
        <div class="flex flex-row justify-end pb-6 px-8 gap-6">
          <button
            @click="closePopup"
            class="border border-gray-300 text-gray-500 rounded hover:bg-gray-100 px-4 py-1"
          >
            {{ cancelText }}
          </button>
          <button
            @click="confirmAction"
            class="bg-pink text-white rounded hover:bg-red-200 py-1 px-6"
            :class="{ 'bg-red-200 pointer-events-none': !eventObj.spaces_available}"
            
          >
            {{ confirmText }}
          </button>
        </div>

      </div>
    </div>
</template>
  
<script setup>

  import { useEventStore } from "@/stores/event.js";

   
  const eventStore = useEventStore()
  const emit = defineEmits(['close', 'confirm'])
  const props = defineProps({
    eventObj: {
      type: Object,
      required: true,
    },
    title: {
      type: String,
      default: 'Popup Title',
    },
    message: {
      type: String,
      default: '',
    },
    confirmText: {
      type: String,
      default: 'Confirm',
    },
    cancelText: {
      type: String,
      default: 'Close',
    }
  })

  const closePopup = ()=> {
    emit('close')
  }
  const confirmAction= ()=> {
    emit('confirm')
  }

  const formatTimeAndTimezone = (time , timezone) => {
    // assuming time is in this format '00:00_EST'
    const formattedTime = eventStore.convertingTime24to12(time);

    return `${formattedTime} ${eventStore.translateTimezoneFromAbreviation(timezone)}`
  }

</script>
  
<style scoped>
</style>