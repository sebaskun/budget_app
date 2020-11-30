import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import router from './router'
// import jQuery from 'jquery'
import VueResource from 'vue-resource'
import VueSelect from 'vue-select'
import Icon from 'vue-awesome/components/Icon.vue'
import VuejsDialog from 'vuejs-dialog'
// import Multiselect from 'vue-multiselect'
// Posiblemente Swal reemplace a VuejsDialog
import VueSweetalert2 from 'vue-sweetalert2'
import SvgIcon from 'vue-svgicon'
import VueFormGenerator from "vue-form-generator"
import "vue-form-generator/dist/vfg.css"

import "./filters"
// import VueHtmlToPaper from 'vue-html-to-paper';

// import Datepicker from 'vue-datepicker-local'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// import 'bootstrap/dist/css/bootstrap.min.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/sass/proyecta.scss'
import 'vue-awesome/icons/arrow-left'
import 'vue-awesome/icons/ellipsis-v'
import 'vue-awesome/icons/ellipsis-h'
import 'vue-awesome/icons/pencil'
import 'vue-awesome/icons/trash'
import 'vue-awesome/icons/check'
import 'vue-awesome/icons/calendar'
import 'vue-awesome/icons/times'
import 'vue-awesome/icons/cog'
import 'vue-awesome/icons/comments'
import 'vue-awesome/icons/minus-square'
import 'vue-awesome/icons/plus-square'
import store from './store'
import AppTitle from "./components/utils/Title.vue"

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
          c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
      }
  }
  return "";
}

Vue.use(BootstrapVue)
Vue.use(VueResource)
// Vue.use(VuejsDialog)
// Vue.use(Multiselect)
Vue.use(SvgIcon, {
  tagName: 'svgicon'
})
Vue.use(VueSweetalert2)
Vue.use(VueFormGenerator)
Vue.component('app-title', AppTitle)

Vue.http.headers.common['X-CSRFToken'] = getCookie('csrftoken')
// Vue.http.options.root = process.env.API_URL;
// Vue.http.interceptors.push(function (request, next) {
//     const authToken = localStorage.getItem('authToken');
//     if (authToken !== null) {
//         request.headers.set('Authorization', 'Bearer ' + authToken);
//     }
//     next(response => {
//         if ((response.status === 401) && (this !== null)) {
//             if (authToken !== null) {
//                 localStorage.removeItem('authToken');
//                 this.$store.dispatch('renewToken', authToken);
//             }
//             this.$store.commit('setIsAuthenticated', false);
//             this.$store.state.authErrorMessage = 'Your session has expired.';
//         }
//     });
// });

Vue.component("v-select", VueSelect)
Vue.component('icon', Icon)

Vue.prototype.$eventHub = new Vue()

String.prototype.capitalize = function() {
  return this.replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
}

var vm = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});
