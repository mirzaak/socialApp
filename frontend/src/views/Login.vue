<template>
  <div
    class="container-fluid d-flex justify-content-center align-items-center vh-100"
  >
    <div class="card">
      <div>
        <form>
          <div class="mt-5 mb-3 ms-5 me-5">
            <label
              style="color: white; font-weight: bold"
              for="exampleInputEmail1"
              class="form-label"
              >Username</label
            >
            <input
              v-model="username"
              type="username"
              class="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
              placeholder="username..."
              style="outline: none !important; box-shadow: none"
            />
            <span
              class="d-flex align-items-center justify-content-center"
              v-if="resp != ''"
            >
              <p class="position-absolute mt-5" v-if="resp" style="color: red">
                {{ resp.username[0] }}
              </p>
            </span>
          </div>
          <div class="mb-3 ms-5 me-5">
            <label
              style="color: white; font-weight: bold"
              for="exampleInputPassword1"
              class="form-label"
              >Password</label
            >
            <input
              v-model="password"
              type="password"
              class="form-control"
              id="exampleInputPassword1"
              placeholder="password..."
              style="outline: none !important; box-shadow: none"
            />
            <span
              class="d-flex align-items-center justify-content-center"
              v-if="resp != ''"
            >
              <p class="position-absolute mt-5" v-if="resp" style="color: red">
                {{ resp.password[0] }}
              </p>
            </span>
          </div>
          <div class="mb-3 ms-5 me-5 d-flex align-items-center flex-column">
            <button
              @click.prevent="submitC()"
              type="submit"
              class="btn btn-dark rounded-pill mt-5 ms-5 me-5"
              id="loginSubmit"
            >
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
    
<script>
import { useProductStore } from "../stores/auth.js";
import { useRouter } from "vue-router";
import { ref } from "vue";
export default {
  setup() {
    const username = ref();
    const password = ref();
    const router = useRouter();
    const store = useProductStore();
    const resp = ref();

    const submitC = async () => {
      localStorage.removeItem("access");

      await fetch("http://127.0.0.1:8000/app/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value,
        }),
      })
        .then((response) => response.json())
        .then((authData) => {
          handleAuthData(authData);
          resp.value = authData;
          store.token = authData.access;
        });
      if (store.token != undefined) {
        router.push("/");
      } else {
        localStorage.removeItem("access");
      }
    };

    function handleAuthData(authData, callback) {
      localStorage.setItem("access", authData.access);
      localStorage.setItem("refresh", authData.refresh);
      localStorage.setItem("name", username.value);

      if (callback) {
        callback();
      }
    }
    return {
      submitC,
      username,
      password,
      resp,
    };
  },
};
</script>
    
<style>
#loginSubmit {
  background: linear-gradient(
    180deg,
    rgba(157, 80, 255, 1) 0%,
    rgba(189, 161, 255, 1) 100%
  );
  border: none;
}
</style>