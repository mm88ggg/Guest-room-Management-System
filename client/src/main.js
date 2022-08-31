import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = false


axios.interceptors.request.use(
    config => {
      if (sessionStorage.getItem('accessToken')) {
        config.headers.Authorization = sessionStorage.getItem('accessToken')
      }
      return config
    },
    err => {
      return Promise.reject(err)
    }
)

axios.interceptors.response.use(
    response => {
      return response
    },
    error => {
      if (error.response) {
        console.log('axios:' + error.response.status)
        switch (error.response.status) {
          case 403:
            sessionStorage.clear()
            router.push('/login')
        }
      }
    }
)

// axios.defaults.baseURL = 'http://127.0.0.1:5001/'
// axios.defaults.baseURL = 'http://1.117.228.153:5001/'
axios.defaults.baseURL = 'http://192.168.1.3:5001/'

Vue.use(VueAxios, axios)

router.beforeEach((to, from, next) => {
  const accessToken = sessionStorage.getItem('accessToken')
  if (accessToken) {
    if (Object.keys(from.query).length !== 0) {
      let redirect = from.query.redirect
      if (to.path === redirect) {
        next()
      } else {
        next({
          path: redirect
        })
      }
    }
  }

  if (accessToken && to.path !== '/login') {
    next()
  } else if (accessToken && to.path === '/login') {
    next({
      path: from.fullPath
    })
  } else if (!accessToken && to.path !== '/login' && to.path !== '/register' && to.path !== '/change_pwd') {
    next('/login')
  } else {
    next()
  }
})

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
