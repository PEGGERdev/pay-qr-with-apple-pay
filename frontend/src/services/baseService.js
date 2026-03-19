export class BaseService {
  constructor({ serviceName = 'service' } = {}) {
    this.serviceName = serviceName
    this._lastError = ''
  }

  lastError() {
    return this._lastError
  }

  clearError() {
    this._lastError = ''
  }

  captureError(error, fallbackMessage) {
    this._lastError = error instanceof Error
      ? error.message
      : fallbackMessage || `Unknown ${this.serviceName} error`
  }
}

export class ApiStateService extends BaseService {
  constructor(api, state, options = {}) {
    super(options)
    this.api = api
    this.state = state
  }

  token() {
    return this.state?.session?.token || ''
  }
}
