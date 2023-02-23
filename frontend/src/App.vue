<template>
<Navbar :key="$route.fullPath" />
</template>

<script setup>
import Navbar from './components/Navbar'


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