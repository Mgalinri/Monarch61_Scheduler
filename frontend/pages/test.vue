<script setup lang="ts">
const items = [{
  slot: 'account',
  label: 'Account'
}, {
  slot: 'password',
  label: 'Password'
}]

const accountForm = reactive({ name: 'Benjamin', username: 'benjamincanac' })
const passwordForm = reactive({ currentPassword: '', newPassword: '' })

function onSubmitAccount() {
  console.log('Submitted form:', accountForm)
}

function onSubmitPassword() {
  console.log('Submitted form:', passwordForm)
}
</script>

<template>
  <UTabs :items="items" class="w-2/3 mx-auto mt-10">
    <template #account="{ item }">
      <Card></Card>
    </template>

    <template #password="{ item }">
      <br>
      <Card></Card>
    </template>
  </UTabs>
</template>

