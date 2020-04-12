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
Vue.prototype.$api_version = process.env.VUE_APP_API_VERSION || 'v2'
Vue.prototype.$api_url = "https://api-" + Vue.prototype.$api_version + ".factrank.org"
Vue.prototype.$branch_version = process.env.VUE_APP_BRANCH_VERSION

import pdf from 'pdfvuer'
// Add the pdf component to Vue
Vue.component('pdf', pdf)

import VueMoment from 'vue-moment'
import moment from 'moment-timezone'
require('moment/locale/nl')
Vue.use(VueMoment, {
        moment,
})

import VueI18n from 'vue-i18n'
Vue.use(VueI18n)

import { languages } from '../lang/index.js'
const messages = {...languages}

Vue.config.productionTip = false

const i18n = new VueI18n({
  locale: (navigator.language || navigator.userLanguage).split('-')[0],
  fallbackLocale: 'en',
  messages
})

// Import the Auth0 configuration
import { domain, clientId } from "../auth_config.json";

// Import the plugin here
import { Auth0Plugin } from "./auth";

// Install the authentication plugin here
Vue.use(Auth0Plugin, {
  domain,
  clientId,
  onRedirectCallback: appState => {
    router.push(
      appState && appState.targetUrl
        ? appState.targetUrl
        : window.location.pathname
    );
  }
});

new Vue({
  i18n,
  router,
  render: h => h(App),
}).$mount('#app')
