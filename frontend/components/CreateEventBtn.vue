<template>
    <div class="flex flex-col flex-1 items-center mt-5 cursor-pointer ">
        <span @click="buttonClicked" class="gap-4 border-2 rounded-xl border-pink py-2 w-1/3 items-center flex flex-row justify-center hover:bg-red-100 hover:text-white">
            <img src="@/assets/icons/add_icon.svg" alt="user icon" class="w-5 h-5 cursor-pointer" />
            <p class="text-lg text-pink">Create new event</p>
        </span>
        <hr class="my-3 w-1/3 h-0.5 bg-gray-100 border-0 dark:bg-gray-700 opacity-50">
    </div>
</template>
<script setup lang="ts">

const emit = defineEmits(['button-clicked']);

const buttonClicked = () => {
    console.log('clicked');
    emit('button-clicked');
}

</script>