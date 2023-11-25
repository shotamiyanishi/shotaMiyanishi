<script setup lang="ts">
import type { Member, Props } from '@/interfaces';
import { inject, computed } from 'vue';
import { RouterLink } from 'vue-router';

const memberList = inject("memberList") as Map<number, Member>;
const props = defineProps<Props>();
const member = computed(
    () : Member => {
        return memberList.get(props.id) as Member;
    }
)
const localNote = computed(
    () : string => {
        let member = memberList.get(props.id) as Member;
        let localNote = member.note;
        if (localNote == undefined) {
            localNote = "not_note"
        } 
        return localNote;
    }
)

const addPoint = () : void => {
    let member = memberList.get(props.id) as Member;
    let point = member.points;
    point += 1;
    member.points = point;
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
        会員情報詳細
    </li>
</ul>
</nav>
<section>
<h2>会員情報詳細</h2>
<p>id: {{ member.id}}</p>
<p>name: {{ member.name}}</p>
<p>email: {{ member.email}}</p>
<p>point: {{ member.points}}</p>
<p>note: {{ localNote}}</p>
<input type = "button" value="加算" v-on:click="addPoint">
</section>
</template>
