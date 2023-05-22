<template>
    <main>
        <div class="container-lg d-flex bg-white border mt-4 p-5 align-items-center justify-content-between"
            style="height:300px">
            <div class="container-lg d-flex align-items-center">
                <div class="card bg-black rounded-circle d-flex align-items-center justify-content-center overflow-hidden"
                    style="width: 200px;height:200px">
                    <img v-if="profile" class="img-thumbnail border-top border-bottom" :src="img + profile.image"
                        style="max-width: 310px;max-height:310px">
                </div>
                <div class="ms-3 d-flex flex-column align-items-center">
                    <h1>{{ profile.user }}</h1>
                    <span class="d-flex flex-row justify-content-between">
                        <h5 class="m-1">Followers</h5>
                        <h5 class="m-1">Following</h5>
                    </span>
                    <span class="d-flex flex-row justify-content-around w-100">
                        <h5 v-if="profile">{{ profile.followers.length }}</h5>
                        <h5 v-if="profile">{{ profile.followings.length }}</h5>
                    </span>
                </div>
            </div>
            <button @click="logOut()" class="btn btn-dark">Log Out</button>
        </div>

        <div v-if="posts" class="container-sm d-flex flex-row flex-wrap align-items-center">
            <div v-for="post in posts.reverse()" :key="post" class="card m-3">
                <div class="card border-0 " style="max-width: 250px;">
                    <p class="d-flex align-items-center card-text m-0 p-2 fw-bold" role="button">
                    <div class="card bg-black rounded-circle d-flex align-items-center justify-content-center overflow-hidden me-2"
                        style="width: 25px;height:25px"><img v-if="post" style="height:25px" :src="img + post.profile.image" alt="">
                    </div>{{ post.user }}</p>
                    <img v-if="post" class="img object-fit-cover" :src="img + post.image" style="min-height: 250px;">
                    <p class="card-text d-flex m-0 p-2">
                    <p role="button" class="fw-bold m-0">{{ post.user }}</p>
                    <p class="ms-2 m-0">{{ post.caption }}</p>
                    </p>
                </div>
            </div>
        </div>
    </main>
</template>
<script setup>
import { useRouter } from "vue-router";
import { ref, shallowRef, onMounted } from "vue";
const profile = ref("");
const img = "http://127.0.0.1:8000/";
const posts = ref();

function logOut() {
  localStorage.clear();
  window.location.href = "http://localhost:8080/";
}

function getFetchOptions(method, body) {
  return {
    method: method === null ? "GET" : method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
    body: body ? body : null,
  };
}

function getProfile() {
  const endpoint = "http://127.0.0.1:8000/app/myprofile/";
  const options = getFetchOptions();
  fetch(endpoint, options)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const validData = isTokenNotValid(data);
      if (validData) {
        profile.value = data;
      }
    });
}

function isTokenNotValid(jsonData) {
  if (jsonData.code && jsonData.code === "token_not_valid") {
    return false;
  }
  return true;
}

function getPosts() {
  const endpoint = "http://127.0.0.1:8000/app/myposts/";
  const options = getFetchOptions();
  fetch(endpoint, options)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const validData = isTokenNotValid(data);
      if (validData) {
        posts.value = data;
      }
    });
}

getPosts();
getProfile();
</script>
