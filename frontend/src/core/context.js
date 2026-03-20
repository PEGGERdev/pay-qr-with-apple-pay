export class AppContext {
  constructor({ state, serviceFactories }) {
    this.state = state
    this._serviceFactories = serviceFactories
    this._services = new Map()
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
}
