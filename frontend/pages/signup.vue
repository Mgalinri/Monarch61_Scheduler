<template>
    <div class="flex flex-row min-h-screen bg-redish-purple gradient-red-orange">
      <div class="flex flex-col w-full items-center mt-36 mb-10">
        <!-- Logo -->
        <img class="h-45 w-1/3 mb-10" src="assets/images/main_logo.png" alt="">
        <!-- Form -->
        <form class="w-1/4" @submit.prevent="login">
            <div class="mb-6">
          <label for="" class="text-white block mb-2.5 text-xl">First Name</label>
          <input 
          type="text" 
          id="email" 
          class="text-xl bg-gray-50 border border-gray-300  text-black rounded-lg block w-full p-2.5 shadow-lg" 
          placeholder="Angel" 
          v-model="fName"
          required />
        </div>
        <div class="mb-6">
          <label for="" class="text-white block mb-2.5 text-xl">Last Name</label>
          <input 
          type="text" 
          id="email" 
          class="text-xl bg-gray-50 border border-gray-300  text-black rounded-lg block w-full p-2.5 shadow-lg" 
          placeholder="Torres" 
          v-model="lName"
          required />
        </div>
        <div class="mb-6">
          <label for="" class="text-white block mb-2.5 text-xl">Email</label>
          <input 
          type="email" 
          id="email" 
          class="text-xl bg-gray-50 border border-gray-300  text-black rounded-lg block w-full p-2.5 shadow-lg" 
          placeholder="Torres" 
          v-model="email"
          required />
        </div>
          <div class="mb-6">
            <label for="" class="text-white block mb-2.5 text-xl">Username</label>
            <input 
            type="text" 
            id="email" 
            class="text-xl bg-gray-50 border border-gray-300  text-black rounded-lg block w-full p-2.5 shadow-lg" 
            placeholder="admin" 
            v-model="username"
            required />
          </div> 
          <div class="mb-6">
            <label for="" 
            class="text-white block mb-2.5 text-xl">Password</label>
            <input 
            pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]){8,}$"
            type="password" 
            id="password" 
            class="text-xl bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 shadow-lg"
            placeholder="•••••••••"
            v-model="password" 
            required />
          </div> 
          <p v-if="errorMessage" class="error text-white font-black"> Username already exists</p>
          <button  @click="navigateTo('/signup')" class="text-white text-xl bg-orange rounded-2xl mt-3 p-2 pt-3 w-full shadow-lg">Sign Up</button>
         
        </form>
       
        <button  @click="navigateTo('/login')" class="text-white text-xl bg-orange rounded-2xl mt-3 p-2 pt-3 w-1/4 shadow-lg">Sign In</button>

       
      </div>
    </div>
  </template>
  <script>
  export default {
    data() {
      return {
        email: "",
        password: "",
        errorMessage: null,
      };
    },
    methods: {
      async login() {
        try {
          const response = await $fetch('/api/signUp', {
            method: 'POST',
            body: { username:this.username, 
                    password:this.password,
                     last_name:this.lName, 
                     first_name:this.fName,
                     email: this.email  },
          })
          .then(async()=>{
            
            await navigateTo('/homepage')
          })
          // Save the user ID or token (for example, in Vuex or a cookie)
          // alert(`Welcome, User ID: ${response.userId}`);
      
        } catch (error) {
          this.errorMessage = error.data.message || 'Login failed. Please try again.';
        }
      },
    },
  };
  </script>