<template>
  <body>
    <div class="container" id="main" ref="main">
      <div class="sign-up">
        <form action="#">
          <h1>Create Account</h1>
          <p>or use your email for registration</p>
          <input type="text" name="txt" placeholder="Username" required="" />
          <input
            type="password"
            name="pswd"
            placeholder="Password"
            required=""
          />
          <input
            type="password"
            name="pswd"
            placeholder="Password"
            required=""
          />
          <button>Sign Up</button>
        </form>
      </div>
      <div class="sign-in">
        <form action="#">
          <h1>Sign in</h1>
          <input
            v-model="username"
            type="username"
            name="username"
            placeholder="username"
            required=""
          />
          <input
            v-model="password"
            type="password"
            name="pswd"
            placeholder="Password"
            required=""
          />

          <button @click.prevent="submitC()">Sign In</button>
        </form>
      </div>
      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-left">
            <h1>Wellcome Back!</h1>
            <p>
              To keep connected with us please login with your personal info
            </p>
            <button ref="signInButton" id="signIn">Sign In</button>
          </div>
          <div class="overlay-right">
            <h1>Hello, Friend</h1>
            <button ref="signUpButton" id="signUp" @click.prevent="submitRegister()">Sign Up</button>
          </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script setup>
import { useProductStore } from "../stores/user.js";
import { useRouter } from "vue-router";
import { ref, onMounted, reactive, computed } from "vue";
import { useVuelidate } from "@vuelidate/core";
import { required, email, minLength, sameAs } from "@vuelidate/validators";
const signUpButton = ref(null);
const signInButton = ref(null);
const main = ref(null);
const username = ref();
const password = ref();
const router = useRouter();
const store = useProductStore();
const resp = ref();

const state = reactive({
      username: "",
      email: "",
      password: {
        password: "",
        confirm: "",
      },
    });

    const rules = computed(() => {
      return {
        username: { required },
        email: { required, email },
        password: {
          password: { required, minLength: minLength(8) },
          confirm: { required, sameAs: sameAs(state.password.password) },
        },
      };
    });

    const v$ = useVuelidate(rules, state);

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
      store.initializeStore();
    });
  if (store.token != undefined) {
    router.push("/");
  } else {
    localStorage.removeItem("access");
  }
};

const submitRegister = () => {
  v$.value.$validate();
  if (!v$.value.$error) {
    fetch("http://127.0.0.1:8000/app/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: state.username,
        email: state.email,
        password: state.password.password,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        resp.value = data;
        if ((data[0] = "success")) {
          router.push({ name: "Login" });
        }
      });
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

onMounted(() => {
  signUpButton.value.addEventListener("click", () => {
    main.value.classList.add("right-panel-active");
  });
  signInButton.value.addEventListener("click", () => {
    main.value.classList.remove("right-panel-active");
  });
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Montserrat:400,800");
* {
  box-sizing: border-box;
}
body {
  align-items: center;
  display: flex;
  justify-content: center;
  flex-direction: column;
  background: #f6f5f7;
  font-family: "monserrat", sans-serif;
  min-height: 100%;
  margin: 10%;
}
.container {
  position: relative !important;
  width: 768px !important;
  max-width: 100% !important;
  min-height: 480px !important;
  background: #fff !important;
  border-radius: 10px !important;
  overflow: hidden !important;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
}
.sign-up,
.sign-in {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  transition: all 0.6s ease-in-out;
}
.sign-up {
  width: 50%;
  opacity: 0;
  z-index: 1;
}
.sign-in {
  width: 50%;
  z-index: 2;
}
form {
  background: #fff !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-direction: column !important;
  padding: 0 50px !important;
  height: 100% !important;
  text-align: center !important;
}
h1 {
  font-weight: bold;
  margin: 0;
}
p {
  font-size: 14px;
  font-weight: 100;
  line-height: 20px;
  letter-spacing: 0.5px;
  margin: 15px 0 20px;
}
input {
  background: #eee;
  padding: 12px 15px;
  margin: 8px 15px;
  width: 100%;
  border-radius: 5px;
  border: none;
  outline: none;
}
a {
  color: #333;
  font-size: 14px;
  text-decoration: none;
  margin: 15px 0;
}
button {
  color: #fff !important;
  background: rgb(35, 32, 101);
  font-size: 12px !important;
  font-weight: bold !important;
  padding: 12px 55px !important;
  margin: 20px !important;
  border-radius: 20px !important;
  border: 1px solid rgb(35, 32, 101);
  outline: none !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  transition: transform 80ms ease-in !important;
  cursor: pointer !important;
}
button:active {
  transform: scale(0.9);
}
#signIn,
#signUp {
  background-color: transparent !important;
  border: 2px solid #fff !important;
}
.container.right-panel-active .sign-in {
  transform: translateX(100%);
}
.container.right-panel-active .sign-up {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
  animation: show 0.6s;
}
@keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }
  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}
.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 0.6s ease-in-out;
  z-index: 100;
}
.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}
.overlay {
  position: relative;
  color: #fff;
  background: rgb(35, 32, 101);
  left: -100%;
  height: 100%;
  width: 200%;
  background: rgb(35, 32, 101);
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}
.container.right-panel-active .overlay {
  transform: translateX(50%);
}
.overlay-left,
.overlay-right {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 40px;
  text-align: center;
  top: 0;
  height: 100%;
  width: 50%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}
.overlay-left {
  transform: translateX(-20%);
}
.overlay-right {
  right: 0;
  transform: translateX(0);
}
.container.right-panel-active .overlay-left {
  transform: translateX(0);
}
.container.right-panel-active .overlay-right {
  transform: translateX(20%);
}
.social-container {
  margin: 20px 0;
}
.social-container a {
  height: 40px;
  width: 40px;
  margin: 0 5px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 50%;
}
</style>