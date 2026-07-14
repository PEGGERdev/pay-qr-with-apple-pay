import RegisteredScreenView from '../views/RegisteredScreenView.vue'

export function getRoutes(featureCatalog) {
  const routes = featureCatalog.flatMap((feature) => (feature.routeDefinitions || []).map((route) => ({
    path: route.path,
    name: route.name,
    component: RegisteredScreenView,
    props: { screen: route.screen },
  })))

  return [
    ...routes,
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ]
}
