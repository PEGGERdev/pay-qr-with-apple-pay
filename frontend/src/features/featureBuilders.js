export function defineRoute(definition) {
  return Object.freeze({ ...definition })
}


export function defineScreen(definition) {
  return Object.freeze({ ...definition })
}


export function defineFeature(definition) {
  return Object.freeze({
    serviceFactories: {},
    actionFactories: {},
    routeDefinitions: [],
    screenDefinitions: [],
    testTargets: [],
    ...definition,
  })
}
