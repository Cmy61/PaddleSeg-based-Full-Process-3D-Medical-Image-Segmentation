import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

//设置iview
import ViewUI from 'view-design'
import ElementUI from 'element-ui';
import 'view-design/dist/styles/iview.css';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ViewUI)
Vue.use(ElementUI)

Vue.config.productionTip = false

import jsCookie from 'js-cookie'
Vue.prototype.$cookie = jsCookie; 

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
