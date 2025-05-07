<template>
    <div class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
      <div class="bg-white rounded-lg shadow-lg w-auto p-6 relative">
        <!-- Close Button & Title -->
        <h2 v-if="title!=''" class="text-lg font-bold mb-4">{{ title }}</h2>
        <!-- Popup Content -->
        <p v-if="message!=''" class="mb-4">{{ message }}</p>
  
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
      title: {
        type: String,
        default: 'Popup Title',
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