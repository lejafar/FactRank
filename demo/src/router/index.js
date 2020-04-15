import Vue from 'vue'
import Router from 'vue-router'

import Landing from '@/pages/Landing'
import FactRanker from '@/pages/FactRanker'
import About from '@/pages/About'
import Search from '@/pages/Search'
import Press from '@/pages/Press'
import Api from '@/pages/Api'

Vue.use(Router)

export default new Router({
  mode: 'history',
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
    }
  ]
})
