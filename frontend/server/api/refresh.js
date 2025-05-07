
export default defineEventHandler(async (event) => {
    async function newAccessToken(){     
        try{
         const cookieRefresh = getCookie(event,'refresh')
         const newCookie = await $fetch("http://localhost:8000/api/token/refresh/",{
             method: 'POST',
             headers:{
                 "Content-Type": "application/json"
             },
             body: {'refresh':cookieRefresh}})
         setCookie(event,'access',newCookie.access)
         return "ok"
         }
        catch(error){
            
            return error
           
        }

   
}
return newAccessToken()})