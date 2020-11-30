import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availablePartidaManpowers: [],
  searchedPartidaManpowers: [],
}

const getters = {
  getAvailablePartidaManpowers: state => state.availablePartidaManpowers,
  getSearchedPartidaManpowers: state => state.searchedPartidaManpowers,
}

const actions = {
  // Search partidas Resource
  searchPartidaManpowers({ commit }, payload, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/manpowers`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedPartidaManpowers', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Requests partidas Resource
  requestPartidaManpowers({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/tasks/${payload.id}/manpowers`).then(response => {
        const data = response.body
        commit('setAvailablePartidaManpowers', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Update Resource Partida
  updatePartidaManpower({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/manpower_task/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updatePartidaManpower', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Add Resource Partida
  addPartidaManpower({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/manpower_task/`, payload).then(response => {
        const data = response.body
        commit('addPartidaManpower', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Delete Resource Partida
  deletePartidaManpower({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.delete(`budget/api/manpower_task/${payload.id}/`).then(response => {
        const data = response.body
        commit('deletePartidaManpower', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}
const mutations = {
  setAvailablePartidaManpowers(state, resources){
    state.availablePartidaManpowers = resources
  },
  addPartidaManpower(state, newData) {
    state.availablePartidaManpowers.push(newData)
  },
  updatePartidaManpower(state, newData) {
    let index = findIndex(state.availablePartidaManpowers, oldData => oldData.id === newData.id)
    state.availablePartidaManpowers.splice(index, 1, newData)
  },
  deletePartidaManpower(state, id) {
    let index = findIndex(state.availablePartidaManpowers, oldData => oldData.id === id)
    state.availablePartidaManpowers.splice(index, 1)
  },
  setSearchedPartidaManpowers(state, resources){
    state.searchedPartidaManpowers = resources
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}