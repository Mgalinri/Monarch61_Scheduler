<template>
    <div v-if="show" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
      <div class="bg-white rounded-lg shadow-lg w-auto p-6 relative">
        <!-- Close Button & Title -->
        <div class="flex justify-between gap-4">
          <h2 v-if="title!=''" class="text-lg font-bold mb-4">{{ title }}</h2>
          <button 
            v-if="exitBtn"
            @click="closePopup" 
            class="flex top-2 right-2 text-gray-600 hover:text-gray-900 mr-2"
            >
            &times;
          </button>
        </div>
        <!-- Popup Content -->
        <p v-if="message!=''" class="mb-4">{{ message }}</p>
        <slot name="additional-content" class="mb-4"></slot>
  
        <!-- Lower Buttons -->
        <div class="mt-4 flex flex-row justify-between space-x-2">
          <button
            v-if="cancelText"
            @click="closePopup"
            
            class="border border-gray-300 text-gray-500 rounded hover:bg-gray-100 px-4 py-1 w-full"
          >
          <!-- border border-gray-300 text-gray-500 rounded hover:bg-gray-100 px-4 py-1
          bg-pink text-white rounded hover:bg-red-200 py-1 px-6 -->
            {{ cancelText }}
          </button>
          <button
            v-if="confirmText"
            @click="confirmAction"
            class="bg-pink text-white px-4 py-2 w-full rounded hover:bg-red-200"
          > 

            {{ confirmText }}
          </button>
        </div>

      </div>
    </div>
</template>
  
  <script>
  export default {
    props: {
      show: {
        type: Boolean,
        required: true,
      },
      title: {
        type: String,
        default: 'Popup Title',
      },
      exitBtn: {
        type: Boolean,
        default: true,
      },
      message: {
        type: String,
        default: null,
      },
      confirmText: {
        type: String,
        default: null,
      },
      cancelText: {
        type: String,
        default: null,
      },
      zIndex: {
        type: Number,
        default: 50,
      },
      
    },
    emits: ['close', 'confirm'],
    methods: {
      closePopup() {
        this.$emit('close');
      },
      confirmAction() {
        this.$emit('confirm');
      },
    },
  };
  </script>
  
  <style scoped>
  </style>