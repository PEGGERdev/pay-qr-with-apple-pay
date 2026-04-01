import { asText } from '../utils/sanitizers'

export function normalizeUser(value) {
  if (!value || typeof value !== 'object') return null
  return {
    id: asText(value.id),
    username: asText(value.username),
    email: asText(value.email),
    displayName: asText(value.display_name || value.displayName || value.username),
  }
}
