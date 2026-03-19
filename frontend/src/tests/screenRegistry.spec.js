import { describe, expect, it } from 'vitest'
import { getComponents } from '../core/registry'
import { createScreenModule, getScreenLifecycle } from '../core/screenRegistry'
import { UI_SLOTS } from '../core/uiElements'

describe('screen registration', () => {
  it('registers lifecycle and slot components', () => {
    const screenId = 'test-screen'
    const module = createScreenModule(screenId)
    const component = { name: 'FakeComponent' }
    const onEnter = () => true

    module.lifecycle({ onEnter })
    module.main({
      id: 'test.component',
      slot: UI_SLOTS.MAIN,
      component,
      buildProps: () => ({ ready: true }),
    })

    const lifecycle = getScreenLifecycle(screenId)
    const components = getComponents(screenId, UI_SLOTS.MAIN)

    expect(lifecycle.onEnter).toBe(onEnter)
    expect(components).toHaveLength(1)
    expect(components[0].component).toBe(component)
  })
})
