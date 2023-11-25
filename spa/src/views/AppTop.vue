<script setup lang = "ts">
import { RouterLink } from 'vue-router';
</script>
<template>
    <h1>TOP</h1>
    <nav id = "breadcrumvbs">
      <ul>
        <li>TOP</li>
      </ul>
    </nav>
    <section>
      <p>
        <RouterLink v-bind:to="{name : 'MemberList'}" >
        会員管理はこちら
        </RouterLink>
      </p>
    </section>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
