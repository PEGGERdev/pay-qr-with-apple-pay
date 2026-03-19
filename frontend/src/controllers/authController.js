import { persistSession } from '../stores/appState'
import { BaseController } from './baseController'

export class AuthController extends BaseController {
  constructor(ctx) {
    super(ctx, 'authService')
  }

  async login(usernameOrEmail, password) {
    const ok = await this.service().login(usernameOrEmail, password)
    if (ok) {
      persistSession(this.ctx.state)
      await this.ctx.controller('payment').loadHistory()
    }
    return ok
  }

  async register(input) {
    const ok = await this.service().register(input)
    if (ok) {
      persistSession(this.ctx.state)
      await this.ctx.controller('payment').loadHistory()
    }
    return ok
  }

  logout() {
    this.service().logout()
    persistSession(this.ctx.state)
  }

  isAuthenticated() {
    return Boolean(this.ctx.state.session.token)
  }
}
