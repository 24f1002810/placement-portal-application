import { createApp } from 'vue'
import App from './App.vue'
import router from '../src/routers/index'
import store from '../src/store/index'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.js'

const app = createApp(App)
app.use(store)
app.use(router)

// Initialize auth on app start
store.dispatch('user/initializeAuth')

app.mount('#app')
