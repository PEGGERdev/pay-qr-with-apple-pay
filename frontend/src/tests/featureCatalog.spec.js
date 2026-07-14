import { describe, expect, it } from 'vitest'

import { collectActionFactories, collectScreenDefinitions, collectServiceFactories, createFeatureCatalog } from '../bootstrap/featureCatalog'


describe('feature catalog', () => {
  it('declares home routes, screens, and action hooks centrally', () => {
    const featureCatalog = createFeatureCatalog()

    expect(featureCatalog.map((feature) => feature.featureId)).toEqual(['home'])
    expect(collectScreenDefinitions(featureCatalog).map((screen) => screen.screen)).toEqual(['home'])
    expect(Object.keys(collectActionFactories(featureCatalog))).toEqual(['auth', 'invoice', 'payment'])
    expect(Object.keys(collectServiceFactories(featureCatalog))).toEqual(['authService', 'invoice', 'payment'])
  })
})
