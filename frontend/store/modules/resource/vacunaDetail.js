import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableVacunaDetails: [],
  selectedVacunaDetail: {},
}

const getters = {
  getVacunaDetails: state => state.availableVacunaDetails,
  getSelectedVacunaDetail: state => state.selectedVacunaDetail,
  getFilteredVacunaDetail: state => filter => state.availableVacunaDetails.filter(item => item.vacuna==filter)
}

const actions = {
  requestVacunaDetails({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/resource/api/vacuna_detail/', {params: search})
      .then(response => {
        const data = response.body.results
        // console.log("result Regimen:", data, "params:", search)
        commit('setVacunaDetails', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addVacunaDetail({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      // console.log("datos:", payLoad)
      Vue.http.post('/resource/api/vacuna_detail/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        dispatch('requestVacunaDetails', {vacunaDetail: payLoad.vacunaDetail})
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateVacunaDetail({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      // console.log("datos:", payLoad)
      Vue.http.patch(`/resource/api/vacuna_detail/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        dispatch('requestVacunaDetails', {vacunaDetail: payLoad.vacunaDetail})
        resolve(data)
      }).catch(error => {
        reject(error) 
      })
    })
  },
}

const mutations = {
    setVacunaDetails(state, results = []) {
    state.availableVacunaDetails = results
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}