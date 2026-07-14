export function defineComponentSpec(definition) {
  return Object.freeze({ ...definition })
}


export function defineSlot(definitions) {
  return Object.freeze([...(definitions || [])])
}


export function defineSlots(slotDefinitions) {
  return Object.freeze({ ...slotDefinitions })
}
