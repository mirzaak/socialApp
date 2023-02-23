import { defineStore } from 'pinia'

export const useProductStore = defineStore('user', {
    state: () => ({
        user: []
    }),

getters: {
 },

 actions: {
    getFetchOptions(method, body){
    return {
        method: method === null ? "GET" : method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
},
    getProfile(){
    const endpoint = 'http://127.0.0.1:8000/app/myprofile/'
    const options = this.getFetchOptions()
    fetch(endpoint, options)
    .then(response=>{
        return response.json()
    })
    .then(data=> {
        const validData = this.isTokenNotValid(data)
        if (validData) {
            this.user = data
            console.log(this.user,'state Data')

        }

    })
},
isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code === "token_not_valid"){
        return false
    }
    return true
}
    }
})