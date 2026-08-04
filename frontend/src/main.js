import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

// Clear persistent session on new tab/window access
if (!sessionStorage.getItem('session_active')) {
  localStorage.removeItem('user');
  localStorage.removeItem('authToken');
  localStorage.removeItem('selected_flight');
  sessionStorage.setItem('session_active', 'true');
}

// Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)

app.use(router)
app.mount('#app')
