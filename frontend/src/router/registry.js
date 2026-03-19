import RegisteredScreenView from '../views/RegisteredScreenView.vue'
import { UI_SCREENS } from '../core/uiElements'
import { ROUTE_PATHS } from './routeSpec'

export function getRoutes() {
  return [
    {
      path: ROUTE_PATHS.HOME,
      name: 'home',
      component: RegisteredScreenView,
      props: { screen: UI_SCREENS.HOME },
    },
  ]
}
