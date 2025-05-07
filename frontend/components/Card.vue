<template>
    <div class="flex flex-row w-[50rem] h-[23rem] bg-white rounded-3xl shadow-md">
    <!-- Image -->
    <div class="w-[23rem] h-[23rem] bg-gray-200 flex items-center justify-center rounded-l-3xl">
     
      <img v-if="!cardObj.image_link" src="@/assets/icons/image_icon.svg" class="w-10 h-10 opacity-50" alt="">
      <img v-if="cardObj.image_link" :src="cardObj.image_link.slice(0,4)==='http' ? cardObj.image_link : '../../uploads/'+cardObj.image_link" class="rounded-l-3xl object-cover h-full w-full" alt="">
    </div>
    <!-- Content -->
    <div class="flex flex-1 flex-col max-w-[27rem] p-4 gap-4">
      <div name="top-icons" class="h-fit items-center flex flex-row gap-4 justify-between">
        <span class="flex flex-col gap-4">
          <p class="font-semibold text-2xl line-clamp-1">{{cardObj.title}}</p>
        </span>
        <div class="flex flex-row gap-4">
          <span name="capacity" class="flex flex-row justify-center gap-2 p-0 m-0">
            <img  class="w-5 h-5" src="@/assets/icons/multiple_users.svg" alt="">
            <p>{{cardObj.spaces_available}}</p>
          </span>
        </div>
      </div>
      <div name="description" class="h-1/5 flex flex-1 flex-col">
        <p class="line-clamp-4">{{cardObj.description}}</p>
      </div>
      <div class="flex flex-col gap-4 h-1/5">
        <span name="Date" class="flex flex-row justify-start gap-2  p-0 m-0">
          <img  class="w-5 h-5" src="@/assets/icons/calendar_icon.svg" alt="">
          <p>{{cardObj.startDate}}</p>
        </span>
        <span name="Time" class="flex flex-row justify-start gap-2  p-0 m-0">
          <img  class="w-5 h-5" src="@/assets/icons/time_icon.svg" alt="">
          <p>{{eventStore.convertingTime24to12(cardObj.time_of_event)}}</p>
        </span>
      </div>
      <div class="flex flex-row gap-4 h-1/6 items-end justify-between">
        <span title="Category" name="category" class="py-1 px-3 bg-pink rounded-full text-white">
          {{cardObj.category}}
        </span>
        <img @click="openPopup()" class="w-10 h-10 cursor-pointer" src="@/assets/icons/arrow_right.svg" alt="">
      </div>
    </div>
    <hr>
  </div>
</template>

<script setup>
  import {useEventStore} from "@/stores/event.js"

  const eventStore = useEventStore()
  const props = defineProps({
    cardObj: {
      type: Object,
      required: true,
    },
  });
  const emit = defineEmits(['event_id']);

  function openPopup() {
    // Emitting the id of this card object
    emit('event_id', props.cardObj.id , props.cardObj.startDate);
  }



</script>