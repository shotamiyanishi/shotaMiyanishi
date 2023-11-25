<script setup lang="ts">
import type { Member, Props } from '@/interfaces';
import { inject, computed, reactive } from 'vue';
import { RouterLink,  useRouter } from 'vue-router';

const memberList = inject("memberList") as Map<number, Member>
const router = useRouter();
const member  = reactive(
    {
        id: 0, 
        name : "",
        email : "@gmail.com",
        points : 0,
        note : ""
    }
)

const onAdd = () : void => {
    console.log(member);
    memberList.set(member.id, member);
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
        会員情報追加
    </li>
</ul>
</nav>

<section>
    <h2>会員情報の追加</h2>
        <p><input type = "text" v-model.number = "member.id" required></p>
        <p><input type = "text" v-model = "member.name"></p>
        <p><input type = "text" v-model = "member.email"></p>
        <p><input type = "text" v-model.number = "member.points"></p>
        <p><input type = "text" v-model = "member.note"></p>
        <p><input type = "submit" value = "reg"  v-on:click= "onAdd"></p>
</section>

</template>
