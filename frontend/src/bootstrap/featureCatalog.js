import { createHomeFeatureRegistration } from '../features/home/featureRegistration'


export function createFeatureCatalog() {
  return [
    createHomeFeatureRegistration(),
  ]
}


export function collectServiceFactories(featureCatalog) {
  return Object.assign({}, ...featureCatalog.map((feature) => feature.serviceFactories || {}))
}


export function collectActionFactories(featureCatalog) {
  return Object.assign({}, ...featureCatalog.map((feature) => feature.actionFactories || {}))
}


export function collectScreenDefinitions(featureCatalog) {
  return featureCatalog.flatMap((feature) => feature.screenDefinitions || [])
}
