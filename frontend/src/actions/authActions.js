import { persistSession } from '../stores/appState'
import { createActionGroup, defineServiceAction, defineStateAction } from './actionFactory'


export function createAuthActions(ctx) {
  return createActionGroup(ctx, {
    login: defineServiceAction({
      serviceId: 'authService',
      method: 'login',
      after: async ({ ctx, result }) => {
        if (result) {
          persistSession(ctx.state)
          await ctx.action('payment').loadHistory()
        }
      },
    }),
    register: defineServiceAction({
      serviceId: 'authService',
      method: 'register',
      after: async ({ ctx, result }) => {
        if (result) {
          persistSession(ctx.state)
          await ctx.action('payment').loadHistory()
        }
      },
    }),
    logout: defineServiceAction({
      serviceId: 'authService',
      method: 'logout',
      after: ({ ctx }) => {
        persistSession(ctx.state)
      },
    }),
    isAuthenticated: defineStateAction(({ ctx }) => Boolean(ctx.state.session.token)),
  })
}
