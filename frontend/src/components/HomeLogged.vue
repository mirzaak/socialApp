<template>
    <main>
        <div v-if="posts" class="container-fluid d-flex flex-column align-items-center justify-content-center">
            <div v-for="post in posts" :key="post" class="card mt-3 d-flex">
                <div class="card border-0" style="width: 450px;">
                    <div class="d-flex align-items-center justify-content-between m-0 p-2 mb-0">
                        <p @click="toProfile(post.user)" class="d-flex align-items-center card-text fw-bold m-0"
                        role="button">
                    <div class="card bg-black rounded-circle d-flex align-items-center justify-content-center overflow-hidden me-2"
                        style="width: 35px;height:35px"><img class="img" style="height:35px"
                            :src="img + post.profilefull.image" alt="">
                        </div>
                        {{ post.user }}</p>
                        <span v-if="myProfile">
                            <svg @click="like(post.pk, post)" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-heart me-2" viewBox="0 0 16 16" id="like">
    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
  </svg>
                        </span>
                    </div>
                    <img class="img-fluid" :src="img + post.image" style="    user-drag: none;
    -webkit-user-drag: none;
    user-select: none;
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;">
                    <p class="card-text d-flex m-0 p-2 pb-0">
                    <p role="button" class="fw-bold m-0">{{ post.user }}</p>
                    <p class="ms-2 m-0">{{ post.caption }}</p>
                    </p>
                    <div v-for="comment in post.comments.slice(-3)" :key="comment">
                        <span class="d-flex">
                            <p style="font-size:12px" class="d-flex m-0 ps-2 pe-2 fw-bold">{{ comment.user }}</p>
                            <p style="font-size:12px" class="d-flex m-0 ps-2 pe-2 text-break">{{ comment.text }}</p>
                        </span>
                    </div>

                    <div class="d-flex align-items-center">
                        <input v-model="post.commentText" id="com" class="d-flex p-2 justify-content-center border-0 m-1"
                            type="text" placeholder="Add a comment..." >
                        <button type="button" class="btn btn-light me-1" style="height:40px"
                            @click.prevent="comment(post.pk, post.commentText, post.comments)">Post</button>
                    </div>
                </div>
            </div>
        </div>
        
    </main>
</template>
<script>
import { useRouter } from "vue-router";
import { ref } from "vue";
import { useProductStore } from "../stores/user";
export default {
  setup() {
    const router = useRouter();
    const img = "http://127.0.0.1:8000";
    const posts = ref();
    const commentText = ref();
    const comments = ref();
    const ProductStore = useProductStore();
    ProductStore.initializeStore();
    const myProfile = ref();
    const likedByMe = ref();

    function like(post_id, post) {
      fetch("http://127.0.0.1:8000/app/like/" + post_id + "/", {
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

    function getLikedByMe() {
      const endpoint = "http://127.0.0.1:8000/app/like/1/";
      const options = getFetchOptions();
      if (ProductStore.isAuthenticated) {
        fetch(endpoint, options)
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            const validData = isTokenNotValid(data);
            if (validData) {
              likedByMe.value = data;
            }
          });
      }
    }

    function comment(post_id, pcom, pComs) {
      fetch("http://127.0.0.1:8000/app/comments/" + post_id + "/", {
        method: "POST", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
        body: JSON.stringify({ text: pcom }),
      })
        .then((response) => response.json())
        .then((data) => {})
        .catch((error) => {});
      pComs.push({ user: localStorage.getItem("name"), text: pcom });
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
              myProfile.value = data;
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

    function toProfile(user) {
      router.push({ name: "Profile", params: { id: user } });
    }

    getPosts();
    getProfile();
    getLikedByMe();
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
      comments,
      myProfile,
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
#like {
  cursor: pointer;
}
</style>