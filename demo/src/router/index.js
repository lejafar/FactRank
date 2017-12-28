import Vue from 'vue'
import Router from 'vue-router'
import FactRanker from '@/components/FactRanker'
import About from '@/components/About'
import Contact from '@/components/Contact'
import Demo from '@/components/Demo'

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
      path: '/contact',
      name: 'Contact',
      component: Contact
    },
    {
      path: '/contact/:name',
      name: 'ContactName',
      component: Contact,
      props: true
    },
    {
      path: '/demo',
      name: 'Demo',
      component: Demo
    }
  ]
})
