function runtimeOrigin() {
  const origin = String(globalThis?.location?.origin || '').trim()
  return origin || 'http://localhost'
}

function hasAbsoluteScheme(value) {
  return /^[a-z][a-z\d+.-]*:\/\//i.test(String(value || '').trim())
}

function normalizeBaseUrl(baseUrl) {
  const raw = String(baseUrl || '').trim()
  if (!raw) {
    return {
      origin: runtimeOrigin(),
      basePath: '',
    }
  }

  const parsed = hasAbsoluteScheme(raw)
    ? new URL(raw)
    : new URL(raw, runtimeOrigin())

  return {
    origin: parsed.origin,
    basePath: parsed.pathname === '/' ? '' : parsed.pathname.replace(/\/+$/, ''),
  }
}

function buildRequestUrl(baseUrl, path) {
  const rawPath = String(path || '').trim()
  if (hasAbsoluteScheme(rawPath)) {
    return rawPath
  }

  const { origin, basePath } = normalizeBaseUrl(baseUrl)
  const normalizedPath = `/${String(rawPath || '/').replace(/^\/+/, '')}`
  const url = new URL(origin)
  url.pathname = `${basePath}${normalizedPath}` || '/'
  return url.toString()
}

function createApiError({ status, method, path, data }) {
  const message = String(data?.detail?.error || data?.detail || data?.error || `Request failed with ${status}`)
  const error = new Error(message)
  error.status = status
  error.method = method
  error.path = path
  error.data = data
  return error
}

export class ApiClient {
  constructor(baseUrl, { onUnauthorized } = {}) {
    this.baseUrl = baseUrl
    this.onUnauthorized = typeof onUnauthorized === 'function' ? onUnauthorized : null
  }

  async request(method, path, { body, token, form = false } = {}) {
    const headers = {}
    let payload
    const hasAuthToken = Boolean(String(token || '').trim())

    if (body !== undefined) {
      if (form) {
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        payload = new URLSearchParams(body).toString()
      } else {
        headers['Content-Type'] = 'application/json'
        payload = JSON.stringify(body)
      }
    }

    if (token) {
      headers.Authorization = `Bearer ${token}`
    }

    const url = buildRequestUrl(this.baseUrl, path)
    const response = await fetch(url, { method, headers, body: payload })
    const text = await response.text()
    let data = {}

    if (text) {
      try {
        data = JSON.parse(text)
      } catch {
        data = { raw: text }
      }
    }

    if (!response.ok) {
      if (response.status === 401 && hasAuthToken && this.onUnauthorized) {
        try {
          this.onUnauthorized({ status: response.status, method, path, data })
        } catch {
          // ignore unauthorized callback failures
        }
      }
      throw createApiError({ status: response.status, method, path, data })
    }

    return data
  }

  get(path, opts = {}) {
    return this.request('GET', path, opts)
  }

  post(path, body, opts = {}) {
    return this.request('POST', path, { ...opts, body })
  }

  postForm(path, body, opts = {}) {
    return this.request('POST', path, { ...opts, body, form: true })
  }
}
