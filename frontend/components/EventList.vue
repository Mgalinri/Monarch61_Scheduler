<template>
<Header/>
<div class="flex flex-col min-h-screen justify-center items-center gap-[10rem] p-5 pt-20">
  <Card v-model="eventObj"/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>
  <Card/>

</div>
<Footer/>
</template>

<script>

export default {
  props: {
    eventList: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selectedEvent: null,
      eventObj: [
        { title: 'Event 1', date: '2024-11-04', description: 'Description 1', time: '9:00 PM'},
      ], // Example: [{ title: 'Event 1', date: '2024-11-04T09:00:00' }]
    };
  },
  methods: {
  },
};
</script>
<style scoped>
</style>