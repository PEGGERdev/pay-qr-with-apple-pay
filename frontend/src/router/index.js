import { createRouter, createWebHistory } from 'vue-router'
import { getRoutes } from './registry'

export function createAppRouter(featureCatalog) {
  return createRouter({
    history: createWebHistory(),
    routes: getRoutes(featureCatalog),
  })
}
