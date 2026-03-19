import { createRouter, createWebHistory } from 'vue-router'
import { getRoutes } from './registry'

export function createAppRouter() {
  return createRouter({
    history: createWebHistory(),
    routes: getRoutes(),
  })
}
