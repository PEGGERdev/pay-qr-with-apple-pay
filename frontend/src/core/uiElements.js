export const UI_SCREENS = Object.freeze({
  HOME: 'home',
})

export const UI_SLOTS = Object.freeze({
  HEADER: 'header',
  MAIN: 'main',
  FOOTER: 'footer',
})

export const UI_COMPONENT_IDS = Object.freeze({
  HOME_HERO: 'home.hero',
  HOME_AUTH: 'home.auth',
  HOME_SCANNER: 'home.scanner',
  HOME_CHECKOUT: 'home.checkout',
  HOME_PREVIEW: 'home.preview',
  HOME_TIMELINE: 'home.timeline',
})

export const UI_LAYOUTS = Object.freeze({
  [UI_SCREENS.HOME]: Object.freeze({
    screen: UI_SCREENS.HOME,
    slots: [UI_SLOTS.HEADER, UI_SLOTS.MAIN, UI_SLOTS.FOOTER],
    screenClass: 'page-shell',
  }),
})
