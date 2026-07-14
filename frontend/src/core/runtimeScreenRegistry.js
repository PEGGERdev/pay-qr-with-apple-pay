import { collectScreenDefinitions } from '../bootstrap/featureCatalog'
import { UI_LAYOUTS } from './uiElements'


export function createScreenRegistry(featureCatalog) {
  const screenDefinitions = collectScreenDefinitions(featureCatalog)
  const byScreen = new Map(screenDefinitions.map((screenDefinition) => [screenDefinition.screen, screenDefinition]))

  return {
    getLifecycle(screen) {
      const definition = byScreen.get(screen)
      return definition ? { screen, onEnter: definition.onEnter || null } : null
    },
    getLayout(screen) {
      return UI_LAYOUTS[screen]
    },
  }
}
