import { BaseController } from './baseController'

export class InvoiceController extends BaseController {
  constructor(ctx) {
    super(ctx, 'invoice')
  }

  parse(rawPayload) {
    return this.service().parse(rawPayload)
  }

  clear() {
    return this.service().clear()
  }
}
