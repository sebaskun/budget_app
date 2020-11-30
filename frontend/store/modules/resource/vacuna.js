import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableListVacunas: [],
  selectedVacuna: {},
}

const getters = {
  getVacunas: state => state.availableListVacunas,
  getSelectedVacuna: state => state.selectedVacuna,
  getFilteredVacuna: state => filter => state.availableListVacunas.filter(item => item.id==filter)
}

const actions = {
  
  requestVacunaInformation({ commit }, vacunaId) {
    Vue.http.get(`resource/api/vacuna/${vacunaId}/`).then(response => {
     commit('setSelectedVacuna', response.body)
    })
  },
  requestAvailableListVacunas({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('resource/api/vacuna/', {params: search})
      .then(response => {
        const data = response.body.results
        // console.log("result Regimen:", data, "params:", search)
        commit('setAvailableListVacunas', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addVacuna({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      // console.log("datos:", payLoad)
      Vue.http.post('resource/api/vacuna/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        dispatch('requestAvailableListVacunas', {vacuna: payLoad.vacuna})
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateVacuna({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      // console.log("datos:", payLoad)
      Vue.http.patch(`resource/api/vacuna/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        dispatch('requestAvailableListVacunas', {vacuna: payLoad.vacuna})
        resolve(data)
      }).catch(error => {
        reject(error) 
      })
    })
  },
}

const mutations = {
  setAvailableListVacunas(state, results = []) {
    state.availableListVacunas = results
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}