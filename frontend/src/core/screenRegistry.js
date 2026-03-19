import { registerComponent } from './registry'
import { UI_SLOTS } from './uiElements'

const screenRegistry = new Map()

function ensureScreen(screen) {
  if (!screenRegistry.has(screen)) {
    screenRegistry.set(screen, {
      screen,
      onEnter: null,
    })
  }
  return screenRegistry.get(screen)
}

export function registerScreenLifecycle({ screen, onEnter }) {
  const target = ensureScreen(screen)
  if (typeof onEnter === 'function') {
    target.onEnter = onEnter
  }
}

export function getScreenLifecycle(screen) {
  const value = screenRegistry.get(screen)
  return value ? { ...value } : null
}

export function createScreenModule(screen) {
  ensureScreen(screen)

  function registerAt(slot, spec) {
    registerComponent({
      screen,
      slot,
      ...spec,
    })
    return api
  }

  const api = {
    header(spec) {
      return registerAt(UI_SLOTS.HEADER, spec)
    },
    main(spec) {
      return registerAt(UI_SLOTS.MAIN, spec)
    },
    footer(spec) {
      return registerAt(UI_SLOTS.FOOTER, spec)
    },
    lifecycle(options) {
      registerScreenLifecycle({ screen, ...(options || {}) })
      return api
    },
  }

  return api
}
