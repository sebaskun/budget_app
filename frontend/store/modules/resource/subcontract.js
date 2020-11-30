import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableSubcontracts: [],
  selectedSubcontract: {},
}

const getters = {
  getSubcontracts: state => state.availableSubcontracts,
  getSelectedSubcontract: state => state.selectedSubcontract,
  getFilteredSubcontract: state => filter => state.availableSubcontracts.filter(item => item.id==filter)
}

const actions = {
  requestSubcontracts({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/resource/api/subcontract/', {params: search})
      .then(response => {
      const data = response.body.results
      const totalRows = response.data.count
      // console.log("result Regimen:", data, "params:", search)
      commit('setSubcontracts', data)
      resolve({data, totalRows})
      }).catch(error => {
        reject(error)
      })
    })
  },
  addSubcontract({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.post('/resource/api/subcontract/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        // commit('setAvailableListRegimen', data)
        dispatch('requestSubcontracts')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateSubcontract({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.patch(`/resource/api/subcontract/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        dispatch('requestSubcontracts')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  removeSubcontract({ commit, dispatch, state }, payload) {
    return new Promise((resolve, reject) => {
        Vue.http.get(`/resource/api/subcontract/${payload.id}/delete`).then(response => {
        const data = response
        // commit('setSelectedBudget', data)
        commit('removeSubcontract', payload.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setSubcontracts(state, results = []) {
    state.availableSubcontracts = results
  },
  removeSubcontract(state, id) {
    let index = findIndex(state.availableSubcontracts, oldSubcontract => oldSubcontract.id === id)
    state.availableSubcontracts.splice(index, 1)
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}