
export default defineEventHandler(async (event) => {
    const data = await readBody(event)

    async function getToken(){
      try{
        
        const response = await $fetch("http://localhost:8000/api/token/",{
          method: 'POST',
          headers:{
              "Content-Type": "application/json"
          },
          body: {username:data.username, password:data.password}})

        setCookie(event,"access",response.access,{
          httpOnly:true,
        })
        setCookie(event,"refresh",response.refresh,{httpOnly:true})
         
        
        const response_2 = await $fetch("http://localhost:8000/api/obtain_usernames",{
           method:'POST',
           headers:{
              "Content-Type": "application/json",
              
              "Authorization": "Bearer "+response.access,
           },
        
         })
         
         
         
       
        return response_2
        }
      catch(error){
        setCookie(event,"access","",{
          httpOnly:true,
        })
        setCookie(event,"refresh","",{httpOnly:true})
        return error
      }
    } 
    return  getToken()

    
})

    // Hardcoded user for simplicity
  

  