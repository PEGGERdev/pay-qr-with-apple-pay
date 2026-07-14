import { clearComponentRegistry } from '../core/registry'
import { clearScreenRegistry, registerScreenDefinitions } from '../core/screenRegistry'
import { collectScreenDefinitions } from './featureCatalog'

export function registerUi(featureCatalog) {
  clearComponentRegistry()
  clearScreenRegistry()
  registerScreenDefinitions(collectScreenDefinitions(featureCatalog))
  return true
}
