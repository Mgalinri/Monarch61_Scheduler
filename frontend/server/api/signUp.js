
export default defineEventHandler(async (event) => {
    const data = await readBody(event)
    
   
    async function getToken(){
      try{
         const response = await $fetch("http://localhost:8000/api/sign_up",{
            method: 'POST',
            headers:{
                "Content-Type": "application/json"
            },
            body: { username:data.username, 
                     password:data.password,
                     last_name:data.last_name, 
                     first_name:data.first_name,
                     email: data.email }})

         
         return{}
        }
      catch(error){
        return error
      }
    } 
    return  getToken()

    
})