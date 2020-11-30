import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableCertificaciones: [],
  selectedCertificacion: {},
}

const getters = {
  getCertificaciones: state => state.availableCertificaciones,
  getSelectedCertificacion: state => state.selectedCertificacion,
  getFilteredCertificacion: state => filter => state.availableCertificaciones.filter(item => item.budget==filter)
}

const actions = {
  requestCertificaciones({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/budget/api/certificacion_budget/', {params: search})
      .then(response => {
        const data = response.body.results
        //console.log("result Certificacion:", data, "params:", search)
        commit('setCertificaciones', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addCertificacion({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.post('/budget/api/certificacion_budget/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        // commit('setAvailableListRegimen', data)
        commit('addCertificacion', data)
        //dispatch('requestCertificaciones')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateCertificacion({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.patch(`/budget/api/certificacion_budget/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('updateCertificacion', data)
        //dispatch('requestCertificaciones')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  deleteCetificacion({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.delete(`/budget/api/certificacion_budget/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('deleteCetificacion', payLoad.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setCertificaciones(state, results = []) {
    state.availableCertificaciones = results
  },

  updateCertificacion(state, newData) {
    let index = findIndex(state.availableCertificaciones, oldData => oldData.id === newData.id)
    state.availableCertificaciones.splice(index, 1, newData)
  },

  deleteCertificacion(state, id) {
    let index = findIndex(state.availableCertificaciones, oldData => oldData.id === id)
    state.availableCertificaciones.splice(index, 1)
  },

  addCertificacion(state, newData) {
    state.availableCertificaciones.push(newData)
  },

}

export default {
  // namespaced: true,
  state,
  getters,
  actions,
  mutations
}