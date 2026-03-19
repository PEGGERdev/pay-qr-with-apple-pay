const componentRegistry = new Map()

function slotKey(screen, slot) {
  return `${screen}:${slot}`
}

export function registerComponent({ screen, slot, id, order = 100, component, buildProps }) {
  const key = slotKey(screen, slot)
  const list = (componentRegistry.get(key) || []).filter((item) => item.id !== id)
  list.push({ id, order, component, buildProps })
  componentRegistry.set(key, list)
}

export function getComponents(screen, slot) {
  const key = slotKey(screen, slot)
  const list = componentRegistry.get(key) || []
  return [...list].sort((a, b) => (a.order - b.order) || a.id.localeCompare(b.id))
}
