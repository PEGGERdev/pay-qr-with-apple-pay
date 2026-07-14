import { describe, expect, it, vi } from 'vitest'

import { createActionGroup, defineServiceAction, defineStateAction } from '../actions/actionFactory'


describe('actionFactory', () => {
  it('builds service actions with after hooks', async () => {
    const serviceMethod = vi.fn().mockResolvedValue('ok')
    const after = vi.fn()
    const ctx = {
      service: vi.fn().mockReturnValue({ save: serviceMethod }),
    }

    const actions = createActionGroup(ctx, {
      save: defineServiceAction({ serviceId: 'payment', method: 'save', after }),
    })

    const result = await actions.save('value')

    expect(result).toBe('ok')
    expect(serviceMethod).toHaveBeenCalledWith('value')
    expect(after).toHaveBeenCalledTimes(1)
  })

  it('builds state actions without service lookup', () => {
    const ctx = { state: { ready: true } }
    const actions = createActionGroup(ctx, {
      isReady: defineStateAction(({ ctx }) => ctx.state.ready),
    })

    expect(actions.isReady()).toBe(true)
  })
})
