import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availablePartidaSubcontracts: [],
  searchedPartidaSubcontracts: [],
}

const getters = {
  getAvailablePartidaSubcontracts: state => state.availablePartidaSubcontracts,
  getSearchedPartidaSubcontracts: state => state.searchedPartidaSubcontracts,
}

const actions = {
  // Search partidas Resource
  searchPartidaSubcontracts({ commit }, payload, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/subcontracts`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedPartidaSubcontracts', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Requests partidas Resource
  requestPartidaSubcontracts({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/tasks/${payload.id}/subcontracts`).then(response => {
        const data = response.body
        commit('setAvailablePartidaSubcontracts', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Update Resource Partida
  updatePartidaSubcontract({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/subcontract_task/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updatePartidaSubcontract', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Add Resource Partida
  addPartidaSubcontract({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/subcontract_task/`, payload).then(response => {
        const data = response.body
        commit('addPartidaSubcontract', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Delete Resource Partida
  deletePartidaSubcontract({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.delete(`budget/api/subcontract_task/${payload.id}/`).then(response => {
        const data = response.body
        commit('deletePartidaSubcontract', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}
const mutations = {
  setAvailablePartidaSubcontracts(state, resources){
    state.availablePartidaSubcontracts = resources
  },
  addPartidaSubcontract(state, newData) {
    state.availablePartidaSubcontracts.push(newData)
  },
  updatePartidaSubcontract(state, newData) {
    let index = findIndex(state.availablePartidaSubcontracts, oldData => oldData.id === newData.id)
    state.availablePartidaSubcontracts.splice(index, 1, newData)
  },
  deletePartidaSubcontract(state, id) {
    let index = findIndex(state.availablePartidaSubcontracts, oldData => oldData.id === id)
    state.availablePartidaSubcontracts.splice(index, 1)
  },
  setSearchedPartidaSubcontracts(state, resources){
    state.searchedPartidaSubcontracts = resources
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}