<template>
  <nav
    v-if="ProductStore.isAuthenticated"
    class="navbar navbar-expand-lg bg-transparent mt-4"
  >
    <div class="container-fluid ms-5 me-5">
      <router-link style="text-decoration: none" to="/"
        ><a
          id="logo"
          class="navbar-brand pe-3 ps-3 pb-2 rounded-pill text-light"
          style="--bs-bg-opacity: 0"
          href="#"
          >socialApp</a
        ></router-link
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item dropdown">
            <a
              v-if="ProductStore.isAuthenticated"
              class="nav-link dropdown-toggle text-white me-5 ms-5"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Create a post
            </a>
            <ul class="dropdown-menu">
              <div class="d-flex flex-column p-3">
                <input
                  class="mb-3 btn btn-dark"
                  @change="handleFileUpload"
                  type="file"
                  id="myElement"
                />
                <label for="text">Caption:</label>
                <input v-model="caption" type="text" />
                <button
                  type="button"
                  class="btn btn-dark mt-3"
                  @click.prevent="createPost"
                >
                  Submit
                </button>
              </div>
            </ul>
          </li>
          <form class="d-flex" role="search">
            <input
              class="form-control me-2 rounded-pill border-0"
              type="search"
              id="btn"
              aria-label="Search"
              v-model="searchText"
            />
            <button
              @click="search()"
              id="submitSearch"
              class="btn btn-outline-light rounded-pill"
              type="submit"
            >
              Search
            </button>
          </form>
        </ul>
        <div class="d-flex align-items-center justify-content-center">
          <router-link
            style="text-decoration: none; margin-right: 10px; color: inherit"
            to="/login"
          >
            <h5
              v-if="!ProductStore.isAuthenticated"
              type="button"
              class="text-white"
            >
              Login
            </h5>
          </router-link>
          <router-link
            style="text-decoration: none; margin-left: 10px; color: inherit"
            to="/register"
          >
            <h5
              v-if="!ProductStore.isAuthenticated"
              type="button"
              class="text-white"
            >
              Register
            </h5>
          </router-link>
          <div class="dropdown">
            <div data-bs-toggle="dropdown">
              <router-link to="/myprofile">
                <div
                  v-if="ProductStore.isAuthenticated"
                  class="card bg-black rounded-circle d-flex align-items-center justify-content-center overflow-hidden"
                  style="width: 50px; height: 50px"
                >
                  <img
                    class="img border-top border-bottom"
                    :src="img + profile.image"
                    style="height: 50px"
                  />
                </div>
              </router-link>
            </div>
            <ul class="dropdown-menu dropdown-menu-lg-end mt-2">
              <router-link style="text-decoration: none" to="/myprofile">
                <li><a class="dropdown-item" href="#">Profile</a></li>
              </router-link>
              <li @click="logOut">
                <a class="dropdown-item" href="#">Log Out</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
  
<script setup>
import { useProductStore } from "../stores/user";
import { useRouter } from "vue-router";
import { ref, shallowRef } from "vue";

const router = useRouter();
const searchText = ref("");
const profile = ref("");
const img = "http://127.0.0.1:8000/";
const file = ref();
const caption = shallowRef("");
const ProductStore = useProductStore();
ProductStore.initializeStore();

function search() {
  router.push({ name: "Searched", params: { search: searchText.value } });
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
  if (ProductStore.isAuthenticated) {
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
}

function isTokenNotValid(jsonData) {
  if (jsonData.code && jsonData.code === "token_not_valid") {
    return false;
  }
  return true;
}
function logOut() {
  localStorage.clear();
  ProductStore.isAuthenticated = false;
  router.push({ name: "Login" });
}

function createPost() {
  const fileInput = document.querySelector("#myElement");
  const formData = new FormData();
  formData.append("image", fileInput.files[0]);
  formData.append("caption", caption.value);
  formData.append("profile", profile.value.pk);
  for (const value of formData.values()) {
  }

  fetch("http://127.0.0.1:8000/app/image_upload/", {
    method: "POST", // or 'PUT'
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {})
    .catch((error) => {});
  router.push("/myprofile");
}

function handleFileUpload(event) {
  file.value = event.target.files[0];
}

getProfile();
</script>
<style>
*,
*:before,
*:after {
  box-sizing: border-box;
}

#btn:focus,
.btn:active {
  outline: none !important;
  box-shadow: none;
}

#logo {
  background: rgba(255, 255, 255, 0.22);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(7.6px);
  -webkit-backdrop-filter: blur(7.6px);
}

#submitSearch {
  left: -80px;
  position: relative;
  background: gray;
}

#submitSearch:hover {
  color: lightgray;
}

#btn {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(11.8px);
  -webkit-backdrop-filter: blur(11.8px);
}
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #2196f3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196f3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>