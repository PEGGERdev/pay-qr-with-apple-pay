import { asText } from '../utils/sanitizers'

function normalizeMethod(value) {
  const method = asText(value).toUpperCase()
  if (['GET', 'POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    return method
  }
  throw new Error(`Unsupported API method: ${value}`)
}

const REGISTRY_BY_KEY = new Map()

function registerApiEndpoint({ key, method, path, authenticated = true, formEncoded = false }) {
  const normalizedKey = asText(key)
  const normalizedPath = asText(path)
  if (!normalizedKey) {
    throw new Error('registerApiEndpoint() requires a key')
  }
  if (!normalizedPath.startsWith('/')) {
    throw new Error(`registerApiEndpoint('${normalizedKey}') requires an absolute path`)
  }
  if (REGISTRY_BY_KEY.has(normalizedKey)) {
    throw new Error(`Duplicate api endpoint key: ${normalizedKey}`)
  }

  const binding = Object.freeze({
    key: normalizedKey,
    method: normalizeMethod(method),
    path: normalizedPath,
    authenticated: Boolean(authenticated),
    formEncoded: Boolean(formEncoded),
  })
  REGISTRY_BY_KEY.set(binding.key, binding)
  return binding
}

export const API_ENDPOINTS = Object.freeze({
  AUTH_LOGIN: 'auth.login',
  AUTH_REGISTER: 'auth.register',
  PAYMENTS_CREATE: 'payments.create',
  PAYMENTS_HISTORY: 'payments.history',
})

registerApiEndpoint({ key: API_ENDPOINTS.AUTH_LOGIN, method: 'POST', path: '/auth/login', authenticated: false })
registerApiEndpoint({ key: API_ENDPOINTS.AUTH_REGISTER, method: 'POST', path: '/auth/register', authenticated: false })
registerApiEndpoint({ key: API_ENDPOINTS.PAYMENTS_CREATE, method: 'POST', path: '/payments' })
registerApiEndpoint({ key: API_ENDPOINTS.PAYMENTS_HISTORY, method: 'GET', path: '/payments/history' })

export function getApiEndpointBinding(key) {
  const binding = REGISTRY_BY_KEY.get(asText(key))
  if (!binding) {
    throw new Error(`Unknown API endpoint key: ${key}`)
  }
  return binding
}
