import Vue from 'vue'
import Router from 'vue-router'

import Landing from '@/pages/Landing'
import FactRanker from '@/pages/FactRanker'
import About from '@/pages/About'
import Search from '@/pages/Search'
import Press from '@/pages/Press'
import Tool from '@/pages/Tool'
import Api from '@/pages/Api'
import Contact from '@/pages/Contact'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: Landing
    },
    {
      path: '/rank',
      name: 'Factranker',
      component: FactRanker
    },
    {
      path: '/tool',
      name: 'Tool',
      component: Tool
    },
    {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '/search',
      name: 'Search',
      component: Search
    },
    {
      path: '/press',
      name: 'Press',
      component: Press
    },
    {
      path: '/api',
      name: 'Api',
      component: Api
    },
    {
      path: '/contact',
      name: 'Contact',
      component: Contact
    }
  ]
})
