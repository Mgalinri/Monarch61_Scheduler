<template>
    <div class="not-found">
      <h1>Oops! Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
      <NuxtLink to="/">Go Back Home</NuxtLink>
    </div>
</template>

<script setup>
useHead({
title: "Page Not Found - My App",
});
</script>

<style scoped>
.not-found {
text-align: center;
padding: 50px;
}
</style>
  