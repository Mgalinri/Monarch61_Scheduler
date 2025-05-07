
// Middleware to check if the user is authenticated
export default defineNuxtRouteMiddleware((to,from) => {
    //Obtain a new access token if the current one is expired redirect to login page

   async function updateToken(){ 
     try {
       const accessCookies = await $fetch("/api/refresh/",{
        method: 'POST',
       })
     }
     catch(error){
        return error
       
     }
   }
    updateToken().then((idea) => {return ;}).catch((error) => {
        console.log(error)
        return navigateTo('/login')})

})