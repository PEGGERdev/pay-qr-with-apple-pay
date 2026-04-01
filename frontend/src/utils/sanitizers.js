export function asText(value) {
  return String(value || '').trim()
}

export function asLowerText(value) {
  return asText(value).toLowerCase()
}

export function asUpperText(value, fallback = '') {
  return asText(value || fallback).toUpperCase()
}
