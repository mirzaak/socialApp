<template>
  <main>
    <div v-if="ProductStore.isAuthenticated">
      <HomeLogged />
    </div>
    <div v-if="!ProductStore.isAuthenticated">
      <HomeLogin />
    </div>
  </main>
</template>
<script>
import HomeLogin from "../components/HomeLogin.vue";
import HomeLogged from "../components/HomeLogged.vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { useProductStore } from "../stores/auth";
export default {
  components: {
    HomeLogin,
    HomeLogged,
  },
  setup() {
    const username = ref();
    const password = ref();
    const router = useRouter();
    const img = "http://127.0.0.1:8000";
    const posts = ref();
    const commentText = ref();
    const ProductStore = useProductStore();
    ProductStore.initializeStore();

    function like(id) {
      fetch("http://127.0.0.1:8000/app/follow/" + id + "/", {
        method: "POST", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {})
        .catch((error) => {});
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

    function getPosts() {
      const endpoint = "http://127.0.0.1:8000/app/image_upload";
      const options = getFetchOptions();
      if (ProductStore.isAuthenticated) {
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
    }

    function isTokenNotValid(jsonData) {
      if (jsonData.code && jsonData.code === "token_not_valid") {
        return false;
      }
      return true;
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

    function comment(post_id) {
      fetch("http://127.0.0.1:8000/app/comments/" + post_id + "/", {
        method: "POST", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
        //                body: JSON.stringify({ text: pcom, user: store.user.pk }),
      })
        .then((response) => response.json())
        .then((data) => {})
        .catch((error) => {});
      window.location.reload();
    }
    function toProfile(user) {
      router.push({ name: "Profile", params: { id: user } });
    }

    getPosts();
    return {
      getPosts,
      posts,
      img,
      like,
      getProfile,
      comment,
      commentText,
      toProfile,
      ProductStore,
    };
  },
};
</script>
<style>
#com:focus,
.btn:active {
  outline: none !important;
  box-shadow: none;
}
</style>