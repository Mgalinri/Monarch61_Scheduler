<template>
    <button
        type="button"
        @click="toggleDropdown"
        :class="hasIcon ? 'pl-8' : ''"
        class="relative group font-medium rounded-md px-4 py-2 text-sm text-gray-900 hover:bg-gray-100"
    >
        {{ selectedOption || defaultLabel }}
        <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class="inline w-4 h-4 ml-1"
        >
        <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M19 9l-7 7-7-7"
        />
        </svg>
        <!-- Dropdown Menu -->
        <div
        v-if="isDropdownOpen"
        @click.outside="closeDropdown"
        class="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-lg py-2 z-20"
        >
            <a type="button" @click="optionSelected(op)" v-for="op in options" class="block px-4 py-2 hover:bg-gray-200 font-medium"
            >
                {{op.name}}
            </a>
        </div>
    </button>
</template>

<script setup>
    import { ref, computed } from 'vue'
    
    const emit = defineEmits(['update:modelValue','on-change']);
    const isDropdownOpen = ref(false)
    const selectedOption = computed(() => props.modelValue || props.defaultLabel);


    function toggleDropdown() {
        isDropdownOpen.value = !isDropdownOpen.value 
    }
    function closeDropdown() {
        isDropdownOpen.value = ref(false);
    }
    function optionSelected(option) {

        emit('update:modelValue', option.id[0]);
        emit('on-change', option.id[0]);
    }

    const props = defineProps({
        modelValue: String, // This is for v-model

        options: {
            type: Array,
            required: true,
        },
        defaultLabel: {
            type: String,
            default: 'Select an option',
        },
        hasIcon: {
            type: Boolean,
            required: false,
            default: false
        }
    });
</script>