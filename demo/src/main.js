import Vue from 'vue'
import App from './App.vue'
import router from './router'

// Bootstrap 4
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)

// Font-Awesome
import 'vue-awesome/icons'
// OR import individual icons
import 'vue-awesome/icons/home'
import 'vue-awesome/icons/star'
import 'vue-awesome/icons/brands/github'
// Import the Icon component
import Icon from 'vue-awesome/components/Icon.vue'
// Add the icon component to Vue
Vue.component('icon', Icon)

import VueMarkdown from 'vue-markdown'
Vue.component('vue-markdown', VueMarkdown)
Vue.prototype.$api_version = process.env.VUE_APP_API_VERSION || 'v0.1.1'

import pdf from 'pdfvuer'
// Add the pdf component to Vue
Vue.component('pdf', pdf)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
