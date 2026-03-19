export class AppContext {
  constructor({ state, serviceFactories, controllerFactories }) {
    this.state = state
    this._serviceFactories = serviceFactories
    this._controllerFactories = controllerFactories
    this._services = new Map()
    this._controllers = new Map()
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

  controller(id) {
    if (!this._controllers.has(id)) {
      const factory = this._controllerFactories[id]
      if (!factory) {
        throw new Error(`Unknown controller_id: ${id}`)
      }
      this._controllers.set(id, factory(this))
    }
    return this._controllers.get(id)
  }
}
