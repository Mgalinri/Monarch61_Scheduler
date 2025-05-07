<template>
    <form class="w-full gap-4" @submit.prevent="createClass">
        <!-- Title -->
        <input
            type="text"
            placeholder="Title here..."
            class="font-bold p-2 bg-transparent w-full text-gray-700 text-2xl focus:outline-none focus:ring-0 border-none mb-2"
            v-model="title"
        />
        <!-- Description -->
        <textarea
            v-model="description"
            placeholder="Type your message..."
            class="ml-[0.25rem] mb-2 p-2 bg-gray-200 rounded p-4 text-lg text-gray-700 resize-none focus:outline-none focus:ring-0 border-none w-full"
            rows="4"
        ></textarea>
        <!-- Small fields -->
        <div class="flex flex-row gap-4 pl-1">
            <!-- Date -->
            <span class="flex flex-row items-center">
                <!-- Icon -->
                <img src="@/assets/icons/calendar_icon.svg" alt="user icon" class="w-4 h-4 z-10 mr-2 cursor-pointer hover:cursor-text" />
                <!-- Date picker -->
                <input class="picker hover:text-pink cursor-pointer" type="date" v-model="startDate" v-on:change="checkDateInputs('start',startDate)">
                <!-- X button -->
                <button type="button" class="ml-[-1rem] z-10 hover:text-pink" @click="cleanDate">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="2"
                        stroke="currentColor"
                        class="w-4 h-4"
                    >
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </span>
            <!-- Instructor -->
            <span title="Instructor" class="flex flex-row items-center">
                <img src="@/assets/icons/user_single_icon.svg" alt="user icon" class="w-4 h-4 mr-[-1.5rem] z-10" />
                <Dropdown v-model="selectedInstructor" :options="intructors"  defaultLabel="Select an instructor" :has-icon="true" />
            </span>
            <!-- Category -->
            <span title="Category" class="flex flex-row items-center">
                <img src="@/assets/icons/category_icon.svg" alt="category icon" class="w-5 h-5 mr-[-1.5rem] z-10" />
                <Dropdown v-model="selectedCategory" :options="categories" defaultLabel="Select a category" :has-icon="true" />
            </span>
            <!-- Capacity -->
            <div title="Capacity" class="flex items-center rounded-md overflow-hidden w-24 gap-2">
                <!-- Icon -->
                <img class="w-5 h-5" src="@/assets/icons/multiple_users.svg" alt="">
                <!-- Number Input -->
                <input 
                    type="number" 
                    v-model="capacity" 
                    class="w-full text-right border-0 border-b-2 border-black focus:border-black focus:ring-0 outline-none w-10"
                />
                <div class="flex flex-col gap-1">
                    <button @click="increaseCapacity" type="button" class="w-3 h-3 p-0 m-0 active:bg-gray-200"><img src="@/assets/icons/arrow_up.svg" alt=""></button>
                    <button @click="decreaseCapacity" type="button" class="w-3 h-3 p-0 m-0 active:bg-gray-200"><img src="@/assets/icons/arrow_down.svg" alt=""></button>
                </div>
            </div>
            <!-- Durations -->
            <div title="Duration" class="flex items-center rounded-md overflow-hidden w-32 gap-2">
                <!-- Icon -->
                <img  class="w-5 h-5" src="@/assets/icons/duration_icon.svg" alt="">
                <!-- Number Input -->
                <select
                    
                    v-model="duration" 
                    class="w-full text-right border-0 border-b-2 border-black focus:border-black focus:ring-0 outline-none w-10"
                >
                <option value=0.5>0.5</option>
                <option value=1>1</option>
                <option value=1.5>1.5</option>
                <option value=2>2</option>
            </select>
                <span>hrs</span>
                <div class="flex flex-col gap-1">
                    <button @click="increaseDuration" type="button" class="w-3 h-3 p-0 m-0 active:bg-gray-200"><img src="@/assets/icons/arrow_up.svg" alt=""></button>
                    <button @click="decreaseDuration" type="button" class="w-3 h-3 p-0 m-0 active:bg-gray-200"><img src="@/assets/icons/arrow_down.svg" alt=""></button>
                </div>
            </div>
            <!-- Time -->
            <div title="Event Time" class="flex items-center rounded-md overflow-hidden w-32 gap-2">
                <!-- Icon -->
                <img class="w-5 h-5 cursor-pointer" src="@/assets/icons/time_icon.svg" @click="openTimePicker" alt="">
                <!-- Number Input -->
                <input 
                    type="time" 
                    v-model="time" 
                    ref="timeInput"
                    class="w-full text-right border-0 border-b-2 border-black focus:border-black focus:ring-0 outline-none w-6"
                    @click="openTimePicker"
                />
            </div>
            
        </div>
        <!-- Repeat every -->
        <span class="flex flex-row items-center mt-2 gap-2 pl-1">
            <span>Repeat every: </span>
            <Dropdown v-model="selectedRepetition" :options="repeat_options" defaultLabel="Select a repetition" :has-icon="false"/>
        </span>
        <!-- Day options -->
        <transition name="fade-in">
            <span v-if="selectedRepetition != 'None' && selectedRepetition != 'Daily'" class="flex flex-row items-center mt-2 gap-2 pl-1">
                <button
                    v-for="day in days"
                    type="button"
                    @click="toggleDay(day)"
                    :key="day"
                    class="px-4 py-1 border rounded-lg transition-all duration-300 active:bg-red-200"
                    :class="selectedDays.has(day) ? 'bg-pink text-white' : 'bg-gray-200 text-black'"
                    >
                    {{ day }}
                </button>
            </span>
        </transition>
        <!-- Until Date -->
        <span v-if="selectedRepetition != 'None'" 
            class="flex flex-row items-center mt-4 ml-1"
            :class="{ 'opacity-50 pointer-events-none': !selectedDays.size && selectedRepetition != 'Daily'}">
            <span class="mr-4">Until: </span>
            <!-- Icon -->
            <!-- Date picker -->
            <input class="picker hover:text-pink cursor-pointer" type="date" v-model="untilDate" v-on:change="checkDateInputs('end',untilDate)">
        </span>

        <!-- Upload Image -->
        <input type="file" @change="handleFileUpload" accept="image/*" class="hidden" ref="fileInput"/>
        <button @dragover.prevent="dragOver"
                @dragleave="dragLeave"
                @drop="handleDrop"
                :class="{ 'bg-gray-400': isDragging }"
                @click="openFilePicker" 
                type="button" 
                class="flex justify-center items-center h-32 mt-6 ml-[0.25rem] p-2 bg-gray-200 rounded p-4 text-lg text-gray-700 resize-none focus:outline-none focus:ring-0 border-none w-full hover:bg-gray-300">
            <!-- Icon -->
            <div class="flex flex-row items-center w-full justify-center" >
                <!-- Dragging an image -->
                <p v-if="isDragging">Drag & drop an image here</p>
                <!-- Upload -->
                <span v-if="!selectedFile && !isDragging" class="flex flex-row items-center gap-2">
                    <p class="hover:text-pink">Upload image</p>
                    <img class="w-5 h-5" src="@/assets/icons/upload_icon.svg" alt="">
                </span>
                <!-- Image Uploaded -->
                <span v-if="selectedFile && !isDragging" class="flex flex-col items-center justify-center gap-2 w-full">
                    <div class="w-1/3">
                        <img :src="previewUrl" class="object-cover h-20 w-full" alt="">
                    </div>
                    <span class="flex flex-row items-center gap-2">
                        <img class="w-5 h-5" src="@/assets/icons/img_icon.svg" alt="">
                        <p class="hover:text-pink"> {{ imageName }}</p>
                        <!-- X button -->
                        <button type="button" class="z-10 hover:text-pink" @click="removeImage">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke-width="2"
                                stroke="currentColor"
                                class="w-4 h-4"
                            >
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </span>
                </span>
            </div>
            
        </button>
        <hr class="h-[0.5px] mt-4 bg-gray-100 border-0 dark:bg-gray-700 opacity-25">
        <!-- Control Buttons -->
        <div class="flex flex-row gap-4 justify-end mt-6 mb-[-1rem]">
            <button type="button" @click="closePopup" class="border border-gray-300 text-gray-500 rounded hover:bg-gray-100 px-4 py-1">Cancel</button>
            <button type="submit" class="bg-pink text-white rounded hover:bg-red-200 py-1 px-6">Add event</button>
        </div>
    </form>
</template>
<script>

    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    
    //Fetch the instructors from the API
    const api = await fetch('http://localhost:8000/api/obtain_instructors', {
        method:'POST',
           headers:{
              "Content-Type": "application/json",
           },})
    const data = await api.json()
    console.log(data)
    const intructors = data.map((instructor) => {return {
        id: instructor[0],
        name : instructor[1]}
    });

    const categories = [
        { id: 'Art', name: 'Art' },
  { id: 'Community', name: 'Community' },
  { id: 'Personal Growth', name: 'Personal Growth' },
  { id: 'Wellness', name: 'Wellness' },
  { id: 'Rooted for Teen Girls', name: 'Rooted for Teen Girls' },
  { id: 'Service', name: 'Service' },
  { id: 'Events/Workshops', name: 'Events/Workshops' },
  { id: 'Trainings', name: 'Trainings' }
    ]
    const repeat_options = [
    { id: 'None', name: 'None' },
  { id: 'Daily', name: 'Daily' },
  { id: 'Weekly', name: 'Weekly' },
  { id: 'Bi-Weekly', name: 'Bi-Weekly' },
  { id: 'Monthly', name: 'Monthly' }
    ]
    export default {
        data() {
            return {
                title: '',
                description: '',
                startDate: '',
                untilDate: '',
                selectedCategory: '',
                selectedInstructor: '',
                categories: categories,
                intructors: intructors,
                capacity: 0,
                duration: 0,
                time: '',
                selectedRepetition: 'None',
                selectedFile: null,
                imageName: '',
                previewUrl: '',
                isDragging: false,
                isPopupVisible: true,
                repeat_options: repeat_options,
                days: days,
                selectedDays: new Set(),
            };
        },
        emits: ['close' , 'warningPopUp', 'create-class'],
        methods: {
            createClass() {
                if (!(this.title && this.description && this.startDate && this.capacity && this.duration && this.selectedCategory && this.selectedInstructor && this.time && this.selectedRepetition)) {
                    this.$emit('warningPopUp',"Check all fields","Please fill out all fields to create a class.");
                    return;
                }
                // no days selected & repetition is either weekly, bi-weekly or monthly
                if (this.selectedDays.size === 0 && (this.selectedRepetition != 'Daily' && this.selectedRepetition != 'None')) {
                    this.$emit('warningPopUp',"Select a day","Please select at least one day for the class.");
                    return;
                }
                if (!this.untilDate && this.selectedRepetition !== 'None') {
                    this.$emit('warningPopUp',"Select a day","Please select an end date for the class.");
                    return;
                }
                console.log(`This is capacity: ${this.capacity}`);
                const formData = {
                    title: this.title,
                    description: this.description,
                    startDate: this.startDate,
                    dateId:0,
                    category: this.selectedCategory,
                    capacity: this.capacity,
                    instructor: this.selectedInstructor,
                    duration: parseFloat(this.duration),
                    time: this.time,
                    imageUrl: (this.imageName)? this.imageName.split('.')[0]+'.webp':''
                };
                console.log(this.startDate)
                const dates = this.generateEventDates(this.startDate, this.untilDate, this.selectedRepetition, Array.from(this.selectedDays));
                console.log(dates)
                formData.dates = dates;

                // converting dates to YYYY-MM-DD
                if (formData.dates.length > 0) {
                    formData.dates.forEach((date,index,arr) => {
                        arr[index] = this.formatDate(date);
                    })
                }
                console.log(formData.dates)
                this.$emit('create-class',formData);
            },
            formatDate(dateString) {
                const dateObj = new Date(dateString);
                const year = dateObj.getFullYear();
                const month = String(dateObj.getMonth() + 1).padStart(2, '0'); // Months are 0-based
                const day = String(dateObj.getDate()).padStart(2, '0');

                return `${year}-${month}-${day}`;
            },
            checkDateInputs(type , _date) {
                if (!['start', 'end'].includes(type)) return; // Ensure valid type

                if (this.checkIfPastDate(_date)) {
                    this.$emit('warningPopUp', "Incorrect date", "Please select a date in the future.");
                    if (type === 'start') this.startDate = '';
                    else this.untilDate = '';
                }
            },
            checkIfPastDate(date) {
                // Current date in YYYY-MM-DD format with one day subtracted
                let currentDate = new Date()
                currentDate.setDate(currentDate.getDate())
                currentDate = currentDate.toISOString().split('T')[0]
                // This function checks if the date is in the past
                if (date < currentDate) {
                  
                    return true
                }
                return false
            },
            generateEventDates(startDate, untilDate, repeatOption, selectedDays = []) {
                const dates = []
                const startDateSplit = startDate.split('-')
                let currentDate = new Date(startDateSplit[0] , startDateSplit[1]-1, startDateSplit[2] );
                const endDateSplit = untilDate.split('-')
                const endDate = new Date(endDateSplit[0] , endDateSplit[1]-1, endDateSplit[2] )
                // Map string days to numerical values (JavaScript Date uses 0=Sunday, 1=Monday, etc.)
                const dayMapping = {
                    "Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6
                };
                const selectedDaysNumbers = selectedDays.map(day => dayMapping[day]);
    
                while (currentDate <= endDate) {
                    switch (repeatOption) {
                        case "D":
                            console.log("daily")
                            dates.push(currentDate.toDateString())
                            break;

                        case "W":
                            if (selectedDaysNumbers.includes(currentDate.getDay())) {
                                dates.push(currentDate.toDateString());
                            }
                            break;

                        case "B":
                            if (selectedDaysNumbers.includes(currentDate.getDay()) && Math.floor((currentDate - new Date(startDate)) / (7 * 24 * 60 * 60 * 1000)) % 2 === 0) {
                                dates.push(currentDate.toDateString());
                            }
                            break;

                        case "M":
                            if (currentDate.getDate() === new Date(startDate).getDate()) {
                                dates.push(currentDate.toDateString());
                            }
                            break;
                    }

                    // Move to the next day
                    currentDate.setDate(currentDate.getDate() + 1);
                }
                console.log(dates)
                return dates; // Format as YYYY-MM-DD
            },
            closePopup() {
                this.$emit('close');
            },
            openDatePicker() {
                this.$refs.datePicker.click(); // Programmatically trigger the click on the hidden date picker
              
            },
            cleanDate(){
                this.startDate = '';
            },
            increaseCapacity() {
                this.capacity += 1;
            },
            decreaseCapacity() {
                if (this.capacity > 0) {
                    this.capacity -= 1;
                }
            },
            increaseDuration() {
                this.duration += parseFloat(0.5);
            },
            decreaseDuration() {
                // this.duration -= .5;
                if (this.duration > 0) {
                    this.duration -= parseFloat(0.5);
                }
            },
            openTimePicker() {
                this.$refs.timeInput.showPicker(); // Opens the time picker
            },
            openFilePicker() {
                this.$refs.fileInput.click(); // Programmatically trigger file input
            },
            handleDrop(event) {
                event.preventDefault();
                this.isDragging = false;
                const file = event.dataTransfer.files[0];
                this.processFile(file);
            },
            processFile(file) {
                if (file && file.type.startsWith("image/")) {
                    this.selectedFile = file;
                    this.imageName = file.name;
                    // Convert file to previewable data URL
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.previewUrl = e.target.result;
                    };
                    reader.readAsDataURL(file);
                    this.uploadImage();
                }else {
                    
                    console.log("Only image files are allowed!");
                }
                
            },
            dragOver(event) {
                event.preventDefault();
                this.isDragging = true;
            },
            dragLeave() {
                this.isDragging = false;
            },
            handleFileUpload(event) {
               
                const file = event.target.files[0];
                if (file && file.type.startsWith("image/")) {
                    this.selectedFile = file;
                    this.imageName = file.name;
                    // Save the preview URL
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.previewUrl = e.target.result;
                    };
                    reader.readAsDataURL(file);
                    // Uploading image to public folder
                    this.uploadImage();
                } else {
                    console.log("Please select a valid image file.");
                    this.selectedFile = null;
                }
            },
            async uploadImage() {
                if (!this.selectedFile) {
                    console.log("No image selected!");
                    return;
                }

                const formData = new FormData();
                formData.append("image", this.selectedFile);

                try {
                    const response = await fetch("/api/upload", {
                        method: "POST",
                        body: formData,
                    });
                    const result = await response.json();
                    console.log(formData)
                    console.log("Image uploaded successfully!");
                } catch (error) {
                    console.error("Upload failed:", error);
                    console.log("Upload failed!");
                }
            },
            removeImage(){
                this.selectedFile = null;
                this.imageName = '';
                this.previewUrl = '';
            },
            toggleDay(day) {
                if (this.selectedDays.has(day)) {
                    this.selectedDays.delete(day); // ✅ Deselect
                } else {
                    this.selectedDays.add(day); // ✅ Select
                }
                // Force reactivity update (since Set is not inherently reactive)
                this.selectedDays = new Set(this.selectedDays);
            }
            
        },
    };
</script>

<style scoped>

input.picker[type="date"] {
  position: relative;
}

input.picker[type="date"]::-webkit-calendar-picker-indicator {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  padding: 0;
  color: transparent;
  background: transparent;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
input[type="time"]::-webkit-calendar-picker-indicator {
    display: none;
    /* margin-right: -30px; */
    -webkit-appearance: none;
}
</style>