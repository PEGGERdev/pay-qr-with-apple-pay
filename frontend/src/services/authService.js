import { normalizeUser } from '../models/userMapper'
import { persistSession } from '../stores/appState'
import { ApiStateService } from './baseService'

export class AuthService extends ApiStateService {
  constructor(api, state, { persistSession: persist = persistSession } = {}) {
    super(api, state, { serviceName: 'auth' })
    this.persistSession = persist
  }

  _applySession(data) {
    if (!data || typeof data !== 'object' || !data.access_token || !data.user) {
      this.captureError('Invalid authentication response', 'Invalid authentication response')
      return false
    }

    this.state.session.token = data.access_token
    this.state.session.user = normalizeUser(data.user)
    this.persistSession(this.state)
    this.clearError()
    return true
  }

  async login(usernameOrEmail, password) {
    try {
      const data = await this.api.post('/auth/login', {
        username_or_email: String(usernameOrEmail || '').trim(),
        password: String(password || ''),
      })
      return this._applySession(data)
    } catch (error) {
      this.captureError(error, 'Login failed')
      return false
    }
  }

  async register({ username, email, password, displayName }) {
    try {
      const data = await this.api.post('/auth/register', {
        username,
        email,
        password,
        display_name: displayName,
      })
      return this._applySession(data)
    } catch (error) {
      this.captureError(error, 'Registration failed')
      return false
    }
  }

  logout() {
    this.state.session.token = ''
    this.state.session.user = null
    this.state.payment.history = []
    this.clearError()
    this.persistSession(this.state)
  }
}
