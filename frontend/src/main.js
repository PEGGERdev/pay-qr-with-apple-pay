import { createApp } from 'vue'
import { createAppRouter } from './router'
import { buildAppContext } from './bootstrap/appBootstrap'
import { APP_CTX_KEY } from './core/injection'
import App from './App.vue'
import './style.css'

const appCtx = buildAppContext()
const app = createApp(App)
const router = createAppRouter()

app.provide(APP_CTX_KEY, appCtx)
app.use(router)
app.mount('#app')
