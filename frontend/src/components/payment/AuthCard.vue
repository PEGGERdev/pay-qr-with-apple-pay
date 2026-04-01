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
    <div class="pill">Step 1 · Secure session</div>
    <h2>Sign in to authorize the payment</h2>
    <p v-if="!props.authState.user">
      Your session protects payment intent creation and keeps the checkout tied to the right account.
    </p>
    <p v-else>
      Signed in as <strong>{{ props.authState.user.displayName || props.authState.user.username }}</strong>. You can continue to invoice review and wallet confirmation.
    </p>

    <div class="segmented-control" v-if="!props.authState.user">
      <button class="segment" :data-active="mode.value === 'login'" type="button" @click="mode.value = 'login'">Sign in</button>
      <button class="segment" :data-active="mode.value === 'register'" type="button" @click="mode.value = 'register'">Create account</button>
    </div>

    <div class="form-grid" v-if="!props.authState.user">
      <div class="field" v-if="mode.value === 'login'">
        <label for="usernameOrEmail">Username or email</label>
        <input id="usernameOrEmail" class="input" autocomplete="username" v-model="form.usernameOrEmail" />
      </div>

      <template v-else>
        <div class="field">
          <label for="username">Username</label>
          <input id="username" class="input" autocomplete="username" v-model="form.username" />
        </div>
        <div class="field">
          <label for="displayName">Display name</label>
          <input id="displayName" class="input" v-model="form.displayName" />
        </div>
        <div class="field">
          <label for="email">Email</label>
          <input id="email" class="input" type="email" autocomplete="email" v-model="form.email" />
        </div>
      </template>

      <div class="field">
        <label for="password">Password</label>
        <input id="password" class="input" type="password" autocomplete="current-password" v-model="form.password" />
      </div>

      <button class="button" type="button" @click="submit">
        {{ mode.value === 'register' ? 'Create account' : 'Sign in' }}
      </button>
    </div>

    <div class="result-box" v-else>
      <div class="detail-grid compact-grid">
        <div class="detail-item">
          <span>Account</span>
          <strong>{{ props.authState.user.email }}</strong>
        </div>
        <div class="detail-item">
          <span>Status</span>
          <strong>Authorized for payment</strong>
        </div>
      </div>
      <button class="button-secondary" type="button" @click="props.onLogout">Log out</button>
    </div>

    <p class="mini-note status-danger" v-if="props.authError">{{ props.authError }}</p>
  </section>
</template>
