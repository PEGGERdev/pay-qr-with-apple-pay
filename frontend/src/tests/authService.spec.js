import { beforeEach, describe, expect, it, vi } from 'vitest'
import { AuthService } from '../services/authService'

describe('AuthService', () => {
  let api
  let persistSession
  let state

  beforeEach(() => {
    api = { post: vi.fn() }
    persistSession = vi.fn()
    state = {
      session: { token: '', user: null },
      payment: { history: [] },
    }
  })

  it('stores session after login', async () => {
    api.post.mockResolvedValue({
      access_token: 'token-1',
      user: {
        id: 'user-1',
        username: 'demo',
        email: 'demo@example.com',
        display_name: 'Demo',
      },
    })

    const service = new AuthService(api, state, { persistSession })
    const ok = await service.login('demo', 'secret')

    expect(ok).toBe(true)
    expect(api.post).toHaveBeenCalledWith('/auth/login', {
      username_or_email: 'demo',
      password: 'secret',
    })
    expect(persistSession).toHaveBeenCalledWith(state)
    expect(state.session.token).toBe('token-1')
    expect(state.session.user.displayName).toBe('Demo')
  })

  it('clears session-related state on logout', () => {
    state.session.token = 'token-1'
    state.session.user = { id: 'user-1' }
    state.payment.history = [{ id: 'pay-1' }]

    const service = new AuthService(api, state, { persistSession })
    service.logout()

    expect(state.session.token).toBe('')
    expect(state.session.user).toBe(null)
    expect(state.payment.history).toEqual([])
    expect(persistSession).toHaveBeenCalledWith(state)
  })
})
