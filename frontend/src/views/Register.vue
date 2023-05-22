<template>
  <div class="container-sm mt-5 d-flex justify-content-center">
    <div class="card" style="width: 25rem">
      <form>
        <div class="d-flex align-items-center flex-column ps-5 pe-5">
          <label
            style="color: white; font-weight: bold"
            for="exampleInputUsername"
            class="form-label align-self-start"
            >Username</label
          >
          <input
            v-model="state.username"
            type="username"
            class="form-control"
            id="exampleInputUsername"
            aria-describedby="emailHelp"
            placeholder="username..."
          />
          <span class="d-flex" v-if="v$.username.$error">
            <p style="color: red">{{ v$.username.$errors[0].$message }}</p>
          </span>
          <span class="d-flex" v-if="resp != ''">
            <p style="color: red; margin: 0">{{ resp.error.username[0] }}</p>
          </span>
        </div>
        <div class="ps-5 pe-5 d-flex align-items-center flex-column">
          <label
            style="color: white; font-weight: bold"
            for="exampleInputEmail1"
            class="form-label align-self-start"
            >Email</label
          >
          <input
            v-model="state.email"
            type="email"
            class="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
            placeholder="email..."
          />
          <span v-if="v$.email.$error">
            <p style="color: red; margin: 0">
              {{ v$.email.$errors[0].$message }}
            </p>
          </span>
        </div>
        <div class="ms-5 me-5 d-flex align-items-center flex-column">
          <label
            style="color: white; font-weight: bold"
            for="exampleInputPassword1"
            class="form-label align-self-start"
            >Password</label
          >
          <input
            v-model="state.password.password"
            type="password"
            class="form-control"
            id="exampleInputPassword1"
            placeholder="password..."
          />
          <span v-if="v$.password.password.$error">
            <p style="color: red; margin: 0">
              {{ v$.password.password.$errors[0].$message }}
            </p>
          </span>
        </div>
        <div class="ms-5 me-5 d-flex align-items-center flex-column">
          <label
            style="color: white; font-weight: bold"
            for="exampleInputPassword2"
            class="form-label align-self-start"
            >Confim Password</label
          >
          <input
            v-model="state.password.confirm"
            type="password"
            class="form-control"
            id="exampleInputPassword2"
            placeholder="password again..."
          />
          <span v-if="v$.password.confirm.$error">
            <p style="color: red; margin: 0">
              {{ v$.password.confirm.$errors[0].$message }}
            </p>
          </span>
        </div>
        <div class="mb-3 ms-5 me-5 d-flex align-items-center flex-column">
          <button
            @click.prevent="submitC()"
            type="submit"
            class="btn btn-dark ms-5 mt-3 me-5 rounded-pill"
            id="loginSubmit"
          >
            Register
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
    
<script>
import { useRoute, useRouter } from "vue-router";
import { useVuelidate } from "@vuelidate/core";
import { required, email, minLength, sameAs } from "@vuelidate/validators";
import { ref, reactive, computed } from "vue";
export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const resp = ref("");

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

    const submitC = () => {
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

    return {
      submitC,
      state,
      v$,
      resp,
    };
  },
};
</script>
    
<style scoped>
p {
  font-size: 15px;
}

#loginSubmit {
  background: linear-gradient(
    180deg,
    rgba(157, 80, 255, 1) 0%,
    rgba(189, 161, 255, 1) 100%
  );
  border: none;
}
</style>