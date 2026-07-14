import { createActionGroup, defineServiceAction, defineStateAction } from './actionFactory'


export function createPaymentActions(ctx) {
  return createActionGroup(ctx, {
    createPaymentRequest: defineServiceAction({ serviceId: 'payment', method: 'createPaymentRequest' }),
    confirmWalletPayment: defineServiceAction({ serviceId: 'payment', method: 'confirmWalletPayment' }),
    loadHistory: defineServiceAction({ serviceId: 'payment', method: 'loadHistory' }),
    getCurrentStep: defineStateAction(({ ctx }) => {
      const invoice = ctx.state.invoice.current
      const session = ctx.state.session
      const payment = ctx.state.payment

      if (invoice && payment.lastResult) {
        return 4
      }
      if (invoice && session.token) {
        return 3
      }
      if (invoice && !session.token) {
        return 2
      }
      return 1
    }),
  })
}
