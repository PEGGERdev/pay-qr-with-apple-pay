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
  <section class="panel auth-panel">
    <div class="step-badge" v-if="!props.authState.user">Step 2</div>
    <div class="step-badge success" v-else>Signed in</div>

    <template v-if="!props.authState.user">
      <h2>Connect your account</h2>
      <p class="step-hint">
        Sign in to complete your payment securely.
      </p>

      <div class="auth-toggle">
        <button 
          class="toggle-btn" 
          :class="{ active: mode.value === 'login' }" 
          type="button" 
          @click="mode.value = 'login'"
        >
          I have an account
        </button>
        <button 
          class="toggle-btn" 
          :class="{ active: mode.value === 'register' }" 
          type="button" 
          @click="mode.value = 'register'"
        >
          New here
        </button>
      </div>

      <div class="form-grid">
        <div class="field" v-if="mode.value === 'login'">
          <label for="usernameOrEmail">Email or username</label>
          <input id="usernameOrEmail" class="input" v-model="form.usernameOrEmail" placeholder="you@example.com" />
        </div>

        <template v-else>
          <div class="field">
            <label for="username">Choose a username</label>
            <input id="username" class="input" v-model="form.username" placeholder="johndoe" />
          </div>
          <div class="field">
            <label for="displayName">Your name</label>
            <input id="displayName" class="input" v-model="form.displayName" placeholder="John Doe" />
          </div>
          <div class="field">
            <label for="email">Email address</label>
            <input id="email" class="input" v-model="form.email" type="email" placeholder="you@example.com" />
          </div>
        </template>

        <div class="field">
          <label for="password">Password</label>
          <input id="password" class="input" type="password" v-model="form.password" placeholder="••••••••" />
        </div>

        <button class="button button-auth" type="button" @click="submit">
          {{ mode.value === 'register' ? 'Create account' : 'Sign in' }}
        </button>
      </div>
    </template>

    <div class="signed-in-panel" v-else>
      <div class="user-info">
        <div class="avatar">{{ props.authState.user.displayName?.[0] || props.authState.user.username?.[0] || '?' }}</div>
        <div class="user-details">
          <span class="user-name">{{ props.authState.user.displayName || props.authState.user.username }}</span>
          <span class="user-email">{{ props.authState.user.email }}</span>
        </div>
      </div>
      <button class="button-secondary" type="button" @click="props.onLogout">Sign out</button>
    </div>

    <p class="error-message" v-if="props.authError">{{ props.authError }}</p>
  </section>
</template>

<style scoped>
.auth-panel {
  background: linear-gradient(180deg, rgba(15, 118, 110, 0.04), rgba(255, 255, 255, 0.8));
}

.step-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(84, 61, 35, 0.08);
  color: var(--muted);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.step-badge.success {
  background: rgba(22, 101, 52, 0.12);
  color: var(--success);
}

.auth-panel h2 {
  margin: 12px 0 6px;
  font-size: 1.5rem;
}

.step-hint {
  color: var(--muted);
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.auth-toggle {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.toggle-btn {
  flex: 1;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid rgba(84, 61, 35, 0.12);
  background: rgba(255, 255, 255, 0.6);
  color: var(--muted);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-btn.active {
  background: var(--accent-soft);
  border-color: var(--accent);
  color: var(--accent-strong);
}

.button-auth {
  padding: 16px 20px;
  font-size: 1rem;
  font-weight: 600;
}

.signed-in-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px;
  border-radius: 16px;
  background: rgba(22, 101, 52, 0.08);
  border: 1px solid rgba(22, 101, 52, 0.2);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 999px;
  background: var(--accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 700;
  text-transform: uppercase;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 600;
  font-size: 1rem;
}

.user-email {
  font-size: 0.85rem;
  color: var(--muted);
}

.error-message {
  margin-top: 16px;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(185, 28, 28, 0.08);
  color: var(--danger);
  font-size: 0.9rem;
}
</style>
