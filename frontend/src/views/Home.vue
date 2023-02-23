<template>
<main>
    <div class="container-fluid d-flex flex-column align-items-center justify-content-center">
        <div v-for="post in posts.reverse()" :key="post" class="card mt-3 d-flex">
            <div class="card border-0" style="max-width: 450px;">
                <p @click="toProfile(post.user)" class="d-flex align-items-center card-text m-0 p-2 fw-bold" role="button"><div class="card bg-black rounded-circle d-flex align-items-center justify-content-center overflow-hidden me-2" style="width: 35px;height:35px"><img class="img-fluid" style="height:35px" :src=" img + post.profilefull.image" alt=""></div>{{ post.user }}</p>
                <img class="img-fluid" :src="img + post.image">
                <p class="card-text d-flex m-0 p-2"><p role="button" class="fw-bold m-0">{{post.user}}</p><p class="ms-2 m-0">{{post.caption }}</p></p>
                <div v-for="comment in post.comments.slice(-1)" :key="comment">
                <span class="d-flex"><p style="font-size:12px" class="d-flex m-0 ps-2 fw-bold">{{ comment.user.user }}</p><p style="font-size:12px" class="d-flex m-0 ps-2">{{ comment.text }}</p></span>
                </div>
                <div class="d-flex align-items-center">
                <input v-model="post.commentText" id="com" class="d-flex p-2 justify-content-center border-0 m-1" type="text" placeholder="Add a comment..." style="width:100%">
                <button type="button" class="btn btn-light me-1" style="height:40px" @click="comment(post.pk, post.commentText)">Post</button>
                </div>
            </div>
        </div>
      </div>
</main>
</template>
<script>
import { useProductStore } from '../stores/user.js'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
export default {
setup(){
    const username = ref()
    const password = ref()
    const router = useRouter()
    const img = 'http://127.0.0.1:8000'
    const posts = ref()
    const store = useProductStore()
    const commentText = ref()

    function like(id){
        fetch('http://127.0.0.1:8000/app/follow/'+id+'/', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function getFetchOptions(method, body){
    return {
        method: method === null ? "GET" : method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
}

    function getPosts(){
    const endpoint = 'http://127.0.0.1:8000/app/image_upload'
    const options = getFetchOptions()
    fetch(endpoint, options)
    .then(response=>{
        return response.json()
    })
    .then(data=> {
        const validData = isTokenNotValid(data)
        if (validData) {
            posts.value = data
            console.log(posts.value)
        }

    })
}

function isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code === "token_not_valid"){
        return false
    }
    return true
}

function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>"
    }
}
function getStore(){
    store.getProfile()
    console.log(store.user,'iiiiiiiiiip')
}


    function getFetchOptions(method, body){
    return {
        method: method === null ? "GET" : method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
}

    function getProfile(){
    const endpoint = 'http://127.0.0.1:8000/app/myprofile/'
    const options = getFetchOptions()
    fetch(endpoint, options)
    .then(response=>{
        return response.json()
    })
    .then(data=> {
        const validData = isTokenNotValid(data)
        if (validData) {

        }

    })
}

function isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code === "token_not_valid"){
        return false
    }
    return true
}

function comment(post_id, pcom){
    console.log(pcom)
    console.log(store.user,'a')
  fetch('http://127.0.0.1:8000/app/comments/' + post_id + '/', {
  method: 'POST', // or 'PUT'
  headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${localStorage.getItem('access')}`
            },
  body: JSON.stringify({text:pcom,user:store.user.pk}),
})
  .then((response) => response.json())
  .then((data) => {
    console.log('Success:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
  window.location.reload();
}
function toProfile(user){
        router.push({ name: 'Profile', params: { id: user }})  
    }

getPosts()
getStore()
return{
    getPosts,
    posts,
    img,
    like,
    getProfile,
    store,
    comment,
    commentText,
    toProfile

}

}  
}
</script>
<style>
body{
    background-color: transparent;
    background-image: linear-gradient(135deg, #492cdd 0%, #AD38E2 100%);
    background-attachment:fixed;
    height:100%;
}
#com:focus,.btn:active {
   outline: none !important;
   box-shadow: none;
}

</style>