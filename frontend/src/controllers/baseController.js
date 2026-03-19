export class BaseController {
  constructor(ctx, serviceId) {
    this.ctx = ctx
    this.serviceId = serviceId
  }

  service() {
    return this.ctx.service(this.serviceId)
  }

  state() {
    return this.ctx.state
  }
}
