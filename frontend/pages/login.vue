<template>
  <div class="flex flex-row min-h-screen bg-redish-purple gradient-red-orange">
    <div class="flex flex-col w-full items-center mt-36 mb-10">
      <!-- Logo -->
      <img class="h-45 w-1/3 mb-10" src="assets/images/main_logo.png" alt="">
     
      <!-- Form -->
      <form class="w-1/4" @submit.prevent="login">
      
        <div class="mb-6">
          <label for="" class="text-white block mb-2.5 text-xl">Username</label>
          <input 
          type="text" 
          id="username" 
          class="text-xl bg-gray-50 border border-gray-300  text-black rounded-lg block w-full p-2.5 shadow-lg" 
          placeholder="admin" 
          v-model="username"
          required />
        </div> 
        <div class="mb-6">
          <label for="" 
          class="text-white block mb-2.5 text-xl">Password</label>
          <input 
          type="password" 
          id="password" 
          class="text-xl bg-gray-50 border border-gray-300 text-gray-900  rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 shadow-lg"
          placeholder="•••••••••"
          v-model="password" 
          required />
        </div> 
        <!-- <div class="flex items-start mb-6">
            <div class="flex items-center h-5">
            <input id="remember" type="checkbox" value="" class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800" required />
            </div>
            <label for="remember" class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">I agree with the <a href="#" class="text-blue-600 hover:underline">terms and conditions</a>.</label>
        </div> -->
         <!-- Invalid credentials message-->
      <div v-if="errorMessage" class="text-white   text-xl mb-4">Invalid Password or Username</div>
        <button type="submit" class="text-white text-xl bg-orange rounded-2xl mt-3 p-2 pt-3 w-full shadow-lg">Sign In</button>

      </form>
      <button  @click="navigateTo('/signup')" class="text-white text-xl bg-orange rounded-2xl mt-3 p-2 pt-3 w-1/4 shadow-lg">Sign Up</button>
    </div>
  </div>
</template>
<script>
import { useUserStore } from '~/stores/user';

export default {

  data() {
    return {
      username: "",
      password: "",
      errorMessage: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await $fetch('/api/login', {
          method: 'POST',
          body: { username: this.username, password: this.password },
        })
        
          const user = useUserStore()

          await user.initializeUserStore(response);
          //Make sure to always use await or return on result of navigateTo when calling it.
          await navigateTo('/')
        
     
    
      } catch (error) {
        this.errorMessage = error || 'Login failed. Please try again.';
      }
    },
  },
};
</script>