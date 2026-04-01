import { asText } from '../utils/sanitizers'

export const SESSION_KEY = 'pay_qr_session_v1'

function normalizedSessionPayload(value) {
  return {
    token: asText(value?.token),
    user: value?.user && typeof value.user === 'object' ? value.user : null,
  }
}

export function createEmptySession() {
  return normalizedSessionPayload(null)
}

export function loadPersistedSession(storage = globalThis?.localStorage) {
  if (!storage) {
    return createEmptySession()
  }

  try {
    const raw = storage.getItem(SESSION_KEY)
    if (!raw) {
      return createEmptySession()
    }
    return normalizedSessionPayload(JSON.parse(raw))
  } catch {
    return createEmptySession()
  }
}

export function applySessionState(state, session) {
  const next = normalizedSessionPayload(session)
  state.session.token = next.token
  state.session.user = next.user
}

export function clearSessionState(state) {
  applySessionState(state, createEmptySession())
}

export function persistSession(state, storage = globalThis?.localStorage) {
  if (!storage) {
    return
  }

  storage.setItem(
    SESSION_KEY,
    JSON.stringify(normalizedSessionPayload(state.session)),
  )
}
