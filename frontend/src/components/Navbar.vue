<template>
    <nav class="navbar navbar-expand-lg bg-transparent mt-4">
    <div class="container-fluid ms-5 me-5">
      <router-link style="text-decoration: none" to="/"><a id="logo" class="navbar-brand pe-3 ps-3 pb-2 rounded-pill text-light" style="--bs-bg-opacity: 0;" href="#">socialApp</a></router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
  
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
  
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
  
          <li class="nav-item dropdown ">
            <a v-if="access" class="nav-link dropdown-toggle text-white me-5 ms-5" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Create a post
            </a>
            <ul class="dropdown-menu">
              <div class="d-flex flex-column p-3">
              <input class="mb-3 btn btn-dark" @change="handleFileUpload" type="file" id="myElement">
              <label for="text">Caption:</label>
              <input v-model="caption" type="text">
              <button type="button" class="btn btn-dark mt-3" @click.prevent="createPost">Submit</button>  
            </div>
            </ul>
          </li>
          <form class="d-flex" role="search">
            <input class="form-control me-2 rounded-pill border-0" type="search" id="btn" aria-label="Search" v-model="searchText">
            <button @click="search()" id="submitSearch" class="btn btn-outline-light rounded-pill" type="submit">Search</button>
        </form>
        </ul>
        <div class="d-flex align-items-center justify-content-center">
          <router-link style="text-decoration: none ; margin-right: 10px; color: inherit;" to="/login"><h5 v-if="!access" type="button" class="text-white" >Login</h5></router-link>
          <router-link style="text-decoration: none ; margin-left: 10px; color: inherit;" to="/register"><h5 v-if="!access" type="button" class="text-white">Register</h5></router-link>
          <div class="dropdown">
          <div data-bs-toggle="dropdown">
            <router-link to="/myprofile">
                  <div v-if="access" class="card bg-black rounded-circle d-flex align-items-center justify-content-center overflow-hidden" style="width: 50px;height:50px">
                    <img v-if="access" class="img border-top border-bottom" :src="img + profile.image" style="height: 50px"></div>
                </router-link>
              </div>
          <ul class="dropdown-menu dropdown-menu-lg-end mt-2">
            <router-link style="text-decoration: none" to="/myprofile"><li><a class="dropdown-item" href="#">Profile</a></li></router-link>
            <li @click="logOut"><a class="dropdown-item" href="#">Log Out</a></li>
          </ul>
        </div>
  
  
        </div>
      </div>
  
    </div>
  </nav>
  
  
  
  
  
    
  <router-view></router-view>
  </template>
  
  <script setup>
  import { useRoute, useRouter  } from 'vue-router'
  import { ref, shallowRef, onMounted } from 'vue'
    const route = useRoute()
    const router = useRouter()
    const searchText = ref('')
    const access = localStorage.getItem('access')
    const refresh = localStorage.getItem('refresh')
    const profile = ref('')
    const img = 'http://127.0.0.1:8000/'
    const file = ref()
    const image = ref('')
    const caption = shallowRef('')
  
  
    function search(){
      router.push({ name: 'Searched', params: { search: searchText.value }})  
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
              profile.value = data
  
          }
  
      })
  }
  
  function isTokenNotValid(jsonData) {
      if (jsonData.code && jsonData.code === "token_not_valid"){
          return false
      }
      return true
  }
  function logOut(){
          localStorage.clear()
          router.push('/login')
      }
  
function createPost(){
    const fileInput = document.querySelector('#myElement') ;
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('caption', caption.value);
    formData.append('profile', profile.value.pk);
    for (const value of formData.values()) {
    console.log(value);
  }
    fetch('http://127.0.0.1:8000/app/image_upload/', {
    method: 'POST', // or 'PUT'
    headers: {
                  "Authorization": `Bearer ${localStorage.getItem('access')}`
              },
    body:formData
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
    router.push('/myprofile')
  }
  
  function handleFileUpload(event){
    file.value = event.target.files[0]
        
  }
  
  
  
  
  getProfile()
  </script>
  <style>
  *, *:before, *:after {
    box-sizing: border-box;
  }
  #btn:focus,.btn:active {
     outline: none !important;
     box-shadow: none;
  }
  #logo{
  background: rgba(255, 255, 255, 0.22);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(7.6px);
  -webkit-backdrop-filter: blur(7.6px);
  }
  #submitSearch{
    left: -80px;
    position: relative;
    background: linear-gradient(180deg, rgba(157,80,255,1) 0%, rgba(189,161,255,1) 100%);
  }
  #submitSearch:hover{
    color: rgb(157,80,255);
  }
  #btn{
  background: rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(11.8px);
  -webkit-backdrop-filter: blur(11.8px);
  }
  
  
    * {
      scrollbar-width: auto;
      scrollbar-color: rgb(157,80,255) #ffffff;
    }
  
  
    *::-webkit-scrollbar {
      width: 13px;
    }
  
    *::-webkit-scrollbar-track {
      background: #ffffff;
    }
  
    *::-webkit-scrollbar-thumb {
      background-color: #8000ff;
      border-radius: 10px;
      border: 3px solid #ffffff;
    }
  </style>