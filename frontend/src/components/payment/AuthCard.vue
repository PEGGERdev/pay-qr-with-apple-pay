<script setup>
import { reactive } from 'vue'

const props = defineProps({
  authState: { type: Object, required: true },
  authError: { type: String, default: '' },
  onLogin: { type: Function, required: true },
  onRegister: { type: Function, required: true },
  onLogout: { type: Function, required: true },
})

const mode = reactive({ value: 'login' })
const form = reactive({
  usernameOrEmail: '',
  username: '',
  email: '',
  password: '',
  displayName: '',
})

async function submit() {
  if (mode.value === 'register') {
    await props.onRegister({
      username: form.username,
      email: form.email,
      password: form.password,
      displayName: form.displayName,
    })
    return
  }

  await props.onLogin(form.usernameOrEmail, form.password)
}
</script>

<template>
  <section class="panel">
    <div class="pill">Authentication</div>
    <h2>Sign in before paying</h2>
    <p v-if="!props.authState.user">
      Payment intent creation is protected behind a bearer session.
    </p>
    <p v-else>
      Signed in as <strong>{{ props.authState.user.displayName || props.authState.user.username }}</strong>.
    </p>

    <div class="button-row" style="margin-top: 18px;" v-if="!props.authState.user">
      <button class="button-secondary" type="button" @click="mode.value = 'login'">Login</button>
      <button class="button-secondary" type="button" @click="mode.value = 'register'">Register</button>
    </div>

    <div class="form-grid" v-if="!props.authState.user">
      <div class="field" v-if="mode.value === 'login'">
        <label for="usernameOrEmail">Username or email</label>
        <input id="usernameOrEmail" class="input" v-model="form.usernameOrEmail" />
      </div>

      <template v-else>
        <div class="field">
          <label for="username">Username</label>
          <input id="username" class="input" v-model="form.username" />
        </div>
        <div class="field">
          <label for="displayName">Display name</label>
          <input id="displayName" class="input" v-model="form.displayName" />
        </div>
        <div class="field">
          <label for="email">Email</label>
          <input id="email" class="input" v-model="form.email" />
        </div>
      </template>

      <div class="field">
        <label for="password">Password</label>
        <input id="password" class="input" type="password" v-model="form.password" />
      </div>

      <button class="button" type="button" @click="submit">
        {{ mode.value === 'register' ? 'Create account' : 'Sign in' }}
      </button>
    </div>

    <div class="result-box" v-else>
      <p>{{ props.authState.user.email }}</p>
      <button class="button-secondary" type="button" @click="props.onLogout">Log out</button>
    </div>

    <p class="mini-note status-danger" v-if="props.authError">{{ props.authError }}</p>
  </section>
</template>
