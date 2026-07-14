export class AppContext {
  constructor({ state, serviceFactories, actionFactories, featureCatalog, screenRegistry }) {
    this.state = state
    this._serviceFactories = serviceFactories
    this._actionFactories = actionFactories
    this._services = new Map()
    this._actions = new Map()
    this.featureCatalog = featureCatalog
    this.screenRegistry = screenRegistry
  }

  service(id) {
    if (!this._services.has(id)) {
      const factory = this._serviceFactories[id]
      if (!factory) {
        throw new Error(`Unknown service_id: ${id}`)
      }
      this._services.set(id, factory(this))
    }
    return this._services.get(id)
  }

  action(id) {
    if (!this._actions.has(id)) {
      const factory = this._actionFactories[id]
      if (!factory) {
        throw new Error(`Unknown action_id: ${id}`)
      }
      this._actions.set(id, factory(this))
    }
    return this._actions.get(id)
  }
}
