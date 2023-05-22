<template>
  <main>
    <div v-for="profile in profile" :key="profile">
      <div
        class="container-lg d-flex bg-white border p-5 align-items-center justify-content-between mt-4"
        style="height: 300px"
      >
        <div class="container-lg d-flex align-items-center">
          <div
            class="card bg-black rounded-circle d-flex align-items-center justify-content-center overflow-hidden"
            style="width: 200px; height: 200px"
          >
            <img
              class="img border-top border-bottom"
              :src="profile.image"
              style="height: 200px"
            />
          </div>

          <div class="ms-3 d-flex flex-column align-items-center">
            <h1 @click="toProfile(profile.user)" role="button">
              {{ profile.user }}
            </h1>
            <span class="d-flex flex-row justify-content-between">
              <h5 class="m-1">Followers</h5>
              <h5 class="m-1">Following</h5>
            </span>
            <span class="d-flex flex-row justify-content-around w-100">
              <h5>{{ profile.followers.length }}</h5>
              <h5>{{ profile.followings.length }}</h5>
            </span>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { useRouter, useRoute } from "vue-router";
import { ref, shallowRef, onMounted } from "vue";
const route = useRoute();
const router = useRouter();
const profile = ref("");
const id = route.params.search;
const img = "http://127.0.0.1:8000/";

function getFetchOptions(method, body) {
  return {
    method: method === null ? "GET" : method,
    headers: {
      "Content-Type": "application/json",
    },
    body: body ? body : null,
  };
}

function getProfile() {
  const endpoint = "http://127.0.0.1:8000/app/search/?search=" + id;
  const options = getFetchOptions();
  fetch(endpoint, options)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      profile.value = data;
    });
}

function toProfile(user) {
  router.push({ name: "Profile", params: { id: user } });
}

getProfile();
</script>
    