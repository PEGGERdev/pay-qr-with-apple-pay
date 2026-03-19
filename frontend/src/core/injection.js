import { inject } from 'vue'

export const APP_CTX_KEY = Symbol('APP_CTX_KEY')

export function useApp() {
  const ctx = inject(APP_CTX_KEY)
  if (!ctx) {
    throw new Error('App context missing')
  }
  return ctx
}
