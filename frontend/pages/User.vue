<template>
    <Header/>
    <div class="flex flex-1 flex-row w-full min-h-screen pt-10 justify-center px-32">
        <div name="profile" class="flex bg-white h-full w-1/3 gap-4 p-4 rounded-2xl shadow-md">
            <div name="round-border" class="border-4 border-black rounded-full p-[10px]">
                <img src="@/assets/icons/user_single_icon.svg" class="w-16 h-16" alt="">
            </div>
            <div class="flex flex-col justify-center">
                <span class="font-bold">{{ first_name }} {{ last_name }} <UBadge v-if="userStore.isUserAdmin()" color="blue" variant="solid">Admin</UBadge></span> 
                <span>{{ email }}</span>
            </div>
        </div>
        <div class="flex flex-col bg-gray-100 flex-1 w-1/3">
            Your events:

            <div class="flex flex-row">
                <span class="bg-red-300 w-[5rem] h-[5rem]">
                </span>
                <div class="flex flex-col justify-center">
                    <span class="font-bold">Event name</span>
                    <span>Event description</span>
                </div>
            </div>

        </div>
    </div>
    <Footer/>

</template>
<script setup>
import { useUserStore } from "@/stores/user.js";

const userStore = useUserStore()
const first_name = ref('')
const last_name = ref('')
const email = ref('')
// const password = ref('')


onMounted(() => {
    document.documentElement.classList.remove('dark');
    first_name.value = userStore.getCurrentUser().firstName
    last_name.value = userStore.getCurrentUser().lastName
    email.value = userStore.getCurrentUser().email

});

</script>