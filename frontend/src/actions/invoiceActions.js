import { createActionGroup, defineServiceAction } from './actionFactory'


export function createInvoiceActions(ctx) {
  return createActionGroup(ctx, {
    parse: defineServiceAction({ serviceId: 'invoice', method: 'parse' }),
    clear: defineServiceAction({ serviceId: 'invoice', method: 'clear' }),
  })
}
