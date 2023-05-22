<template>
  <Navbar v-if="ProductStore.isAuthenticated" />

  <router-view></router-view>
</template>

<script setup>
import { useProductStore } from "./stores/user";
import Navbar from "./components/Navbar";

const ProductStore = useProductStore();

ProductStore.initializeStore();
</script>
<style>
html,
body {
  margin: 0;
  padding: 0;
  background-color: rgb(192, 192, 192) !important;
}
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
</style>