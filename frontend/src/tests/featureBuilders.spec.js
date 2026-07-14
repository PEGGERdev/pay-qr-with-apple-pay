import { describe, expect, it } from 'vitest'

import { defineFeature, defineRoute, defineScreen } from '../features/featureBuilders'
import { defineComponentSpec, defineSlot, defineSlots } from '../features/screenBuilders'


describe('feature builders', () => {
  it('creates frozen feature, route, and screen declarations', () => {
    const feature = defineFeature({ featureId: 'demo' })
    const route = defineRoute({ path: '/', name: 'home', screen: 'home' })
    const screen = defineScreen({ screen: 'home' })

    expect(Object.isFrozen(feature)).toBe(true)
    expect(Object.isFrozen(route)).toBe(true)
    expect(Object.isFrozen(screen)).toBe(true)
  })

  it('creates frozen slot and component declarations', () => {
    const component = defineComponentSpec({ id: 'demo.card', component: { name: 'Card' } })
    const slot = defineSlot([component])
    const slots = defineSlots({ main: slot })

    expect(Object.isFrozen(component)).toBe(true)
    expect(Object.isFrozen(slot)).toBe(true)
    expect(Object.isFrozen(slots)).toBe(true)
    expect(slots.main[0].id).toBe('demo.card')
  })
})
