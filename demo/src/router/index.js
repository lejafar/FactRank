import Vue from 'vue'
import Router from 'vue-router'
import FactRanker from '../components/FactRanker'
import About from '../components/About'
import Search from '../components/Search'
import Press from '../components/Press'
import Demo from '../components/Demo'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
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
      path: '/demo',
      name: 'Demo',
      component: Demo
    }
  ]
})
