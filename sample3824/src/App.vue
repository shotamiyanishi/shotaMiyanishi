<script setup lang="ts">
import {ref} from "vue"
const num_seq_init : number[] = [];
let num_seq = ref(num_seq_init);

const add = () : void => {
  const num1 = document.getElementById("num1") as HTMLInputElement;
  const num2 = document.getElementById("num2") as HTMLInputElement;
  const result : number = Number(num1.value) + Number(num2.value);
  num_seq.value.push(result);
}

const sub = () : void => {
  const num1 = document.getElementById("num1") as HTMLInputElement;
  const num2 = document.getElementById("num2") as HTMLInputElement;
  const result : number = Number(num1.value) - Number(num2.value);
  num_seq.value.push(result);
}

const times = () : void => {
  const num1 = document.getElementById("num1") as HTMLInputElement;
  const num2 = document.getElementById("num2") as HTMLInputElement;
  const result : number = Number(num1.value) * Number(num2.value);
  num_seq.value.push(result);
}

const div = () : void => {
  const num1 = document.getElementById("num1") as HTMLInputElement;
  const num2 = document.getElementById("num2") as HTMLInputElement;
  const result : number = Number(num1.value) / Number(num2.value);
  num_seq.value.push(result);
}

const reset = () : void => {
  num_seq.value = []
}

</script>

<template>
  num1:<input type = "text" id = "num1" /> <br>
  num2:<input type = "text" id = "num2" /> <br>
  <input type = "button" name = "add" value = "+" v-on:click= "add">
  <input type = "button" name = "sub" value = "-" v-on:click= "sub">
  <input type = "button" name = "times" value = "*" v-on:click= "times">
  <input type = "button" name = "div" value = "÷" v-on:click= "div"><br>
  <input type = "button" name = "reset" value = "reset" v-on:click= "reset">
  <table>
    <tr v-for= "num, index in num_seq">
      <td v-if = "index % 2 == 0">
        <span class = "odd">{{num}}</span>
      </td>
      <td v-if = "index % 2 != 0">
        {{ num}}
      </td>
    </tr>
  </table>
</template>

<style scoped>
span.odd {
  background-color: yellow; /* Change this to the desired background color */
}
</style>
