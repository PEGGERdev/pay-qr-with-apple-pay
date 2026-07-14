import { getApiEndpointBinding } from '../api/registry'
import { ApiStateService } from './baseService'
import { asText } from '../utils/sanitizers'

function buildPath(pathTemplate, params = {}) {
  const source = asText(pathTemplate)
  const path = source.replace(/\{([a-zA-Z0-9_]+)\}/g, (_full, name) => {
    const normalized = asText(params[name])
    if (!normalized) {
      throw new Error(`Missing path parameter: ${name}`)
    }
    return encodeURIComponent(normalized)
  })

  if (/\{[a-zA-Z0-9_]+\}/.test(path)) {
    throw new Error(`Unresolved path template: ${source}`)
  }

  return path
}

export class ApiGatewayService extends ApiStateService {
  constructor(api, state) {
    super(api, state, { serviceName: 'api' })
  }

  _resolveToken({ authenticated, token }) {
    const override = asText(token)
    if (!authenticated) {
      return override
    }

    const activeToken = override || asText(this.token())
    if (!activeToken) {
      throw new Error('Authentication required')
    }
    return activeToken
  }

  async request(endpointKey, { params = {}, body = undefined, token = '', formEncoded } = {}) {
    const binding = getApiEndpointBinding(endpointKey)
    const path = buildPath(binding.path, params)
    const resolvedToken = this._resolveToken({ authenticated: binding.authenticated, token })
    const useFormEncoded = typeof formEncoded === 'boolean' ? formEncoded : binding.formEncoded

    if (binding.method === 'GET') {
      return this.api.get(path, { token: resolvedToken })
    }
    if (binding.method === 'POST') {
      if (useFormEncoded) {
        return this.api.postForm(path, body || {}, { token: resolvedToken })
      }
      return this.api.post(path, body || {}, { token: resolvedToken })
    }
    throw new Error(`Unsupported API method: ${binding.method}`)
  }
}
