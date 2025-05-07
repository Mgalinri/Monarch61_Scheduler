<template>
    <div v-if="isSticky" class="font-sans bg-red-500 h-20 fixed"></div>
    <Header />    
    <!-- <Dropdown :options="options" dropdownName="Select an option" v-model="selectedOption" /> -->
    <div :class="{ 'pt-32': isSticky }" class="negative-margin font-sans min-h-screen max-w-8xl mx-auto flex flex-col justify-center items-center" >
        <span class="text-3xl font-bold mb-4">Attend a Class</span>
        <br>
        <section class="text-2xl text-center w-3/4 tracking-wide font-extralight">Scheduling a class or a spot in a group is easy! Simply click on the class below that you want to register for and follow the prompts to enroll in classes online or call us at 479-410-4225 to save your spot. Classes are free but donations to replenish supplies are always welcome! Any special workshops with a fee will be specified in the class description. We are always adding new classes; check the calendar often to see what’s new!</section>

        <router-link to="/event-dashboard">
            <button class="text-white text-2xl bg-pink rounded-3xl mt-14 p-2 shadow-lg w-40">Calendar</button>
        </router-link>
    </div>
    <!--
    <div class="font-sans text-white bg-pink min-h-screen max-w-8xl mx-auto flex flex-col justify-center items-center">
        <span class="text-3xl font-bold mb-4">Quiz</span>
        <br>
        <section class=" text-2xl text-center w-3/4 tracking-wide font-extralight">This personalized quiz is designed to help women facing challenges such as domestic violence, sexual assault, or generational poverty find the support they need. By answering a few questions about your current situation, you'll receive tailored recommendations for materials, tools, and resources that can empower you on your path to healing and growth. All responses are confidential, and the goal is to provide meaningful guidance to help you take the next steps toward a brighter future.</section>

        <router-link to="#">
            <button class="text-white text-2xl bg-black rounded-3xl mt-14 p-2 shadow-lg  w-48">Take a quiz</button>
        </router-link>
    </div>
    -->
    <!-- Footer -->
    <Footer/>
</template>

<script setup>
   import { useUserStore } from "@/stores/user.js";
   const userStore = useUserStore()
    onBeforeMount(() => {
   
  
     if (userStore.users.firstName == undefined) {
     // Redirect to login page if user is not logged in
     navigateTo('/login')
     }
   });


    import { ref } from 'vue'

    const isSticky = ref(false)
    const selectedOption = ref(null)

    const options = ['Option 1', 'Option 2', 'Option 3'];

    function handleOptionSelected(option) {
        console.log('Parent received:', option);
        selectedOption.value = option; // Update the parent's state
    }
    onMounted(() => {
        document.documentElement.classList.remove('dark');
    });

</script>

<style scoped>
    .negative-margin {
        margin-top: -100px;
    }
    .content {
        padding-top: 300px; /* Adjust the padding-top value to match the height of the sticky header */
    }

</style>
