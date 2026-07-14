import { AppContext } from '../core/context'
import { collectActionFactories, collectServiceFactories, createFeatureCatalog } from './featureCatalog'
import { createAppState, persistSession } from '../stores/appState'
import { ApiClient } from '../services/apiClient'
import { ApiGatewayService } from '../services/apiGatewayService'
import { registerUi } from './uiRegistrations'
import { createScreenRegistry } from '../core/runtimeScreenRegistry'

export function buildAppContext() {
  const state = createAppState()
  const featureCatalog = createFeatureCatalog()

  function handleUnauthorized() {
    state.session.token = ''
    state.session.user = null
    persistSession(state)
  }

  const screenRegistry = createScreenRegistry(featureCatalog)
  const ctx = new AppContext({
    state,
    featureCatalog,
    serviceFactories: {
      apiClient: (ctx) => new ApiClient(ctx.state.config.apiBaseUrl, { onUnauthorized: handleUnauthorized }),
      apiGateway: (ctx) => new ApiGatewayService(ctx.service('apiClient'), ctx.state),
      ...collectServiceFactories(featureCatalog),
    },
    actionFactories: collectActionFactories(featureCatalog),
    screenRegistry,
  })

  registerUi(featureCatalog)
  return ctx
}
