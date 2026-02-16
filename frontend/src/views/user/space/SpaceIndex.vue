<script setup>
import {useRoute} from "vue-router";

const route = useRoute();

</script>

<template>
space:{{route.params.user_id}}
</template>

<style scoped>

</style>
