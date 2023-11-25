<script setup lang="ts">
import type { Member, Props } from '@/interfaces';
import { inject, computed, reactive , ref} from 'vue';
import { RouterLink,  useRouter } from 'vue-router';

const id_radio = ref();
const memberList = inject("memberList") as Map<number, Member>
const router = useRouter();

const onDelete = () : void => {
    console.log(id_radio.value);
    memberList.delete(id_radio.value);
    router.push({name : "MemberList"})
}

</script>

<template>
<h1>会員管理</h1>
<nav id = "breadcrumbs">
<ul>
    <li>
    <RouterLink :to = "{name:'AppTop'}">
        TOP
    </RouterLink>
    </li>
    <li>
    <RouterLink :to = "{name:'MemberList'}">
        会員リスト
    </RouterLink>
    </li>
    <li>
        会員情報削除
    </li>
</ul>
</nav>

<section>
    <h2>会員id</h2>
    <p v-for = "[id, member] in memberList" :key = "id + 'member'"><input type = "radio" name = "id" :value = "id" v-model = "id_radio">{{ member.id }}</p>
    {{id_radio}} 
    <input type = "button" value = "del" v-on:click="onDelete">
</section>

</template>
