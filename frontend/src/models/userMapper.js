export function normalizeUser(value) {
  if (!value || typeof value !== 'object') return null
  return {
    id: String(value.id || '').trim(),
    username: String(value.username || '').trim(),
    email: String(value.email || '').trim(),
    displayName: String(value.display_name || value.displayName || value.username || '').trim(),
  }
}
