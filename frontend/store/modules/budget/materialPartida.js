import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availablePartidaMaterials: [],
  searchedPartidaMaterials: [],
}

const getters = {
  getAvailablePartidaMaterials: state => state.availablePartidaMaterials,
  getSearchedPartidaMaterials: state => state.searchedPartidaMaterials.filter(item => item.type_material=="S"),
}

const actions = {
  // Search partidas Resource
  searchPartidaMaterials({ commit }, payload, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/materials`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedPartidaMaterials', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Requests partidas Resource
  requestPartidaMaterials({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/tasks/${payload.id}/materials`).then(response => {
        const data = response.body
        commit('setAvailablePartidaMaterials', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Update Resource Partida
  updatePartidaMaterial({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/material_task/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updatePartidaMaterial', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Add Resource Partida
  addPartidaMaterial({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/material_task/`, payload).then(response => {
        const data = response.body
        commit('addPartidaMaterial', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Delete Resource Partida
  deletePartidaMaterial({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.delete(`budget/api/material_task/${payload.id}/`).then(response => {
        const data = response.body
        commit('deletePartidaMaterial', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}
const mutations = {
  setAvailablePartidaMaterials(state, resources){
    state.availablePartidaMaterials = resources
  },
  addPartidaMaterial(state, newData) {
    state.availablePartidaMaterials.push(newData)
  },
  updatePartidaMaterial(state, newData) {
    let index = findIndex(state.availablePartidaMaterials, oldData => oldData.id === newData.id)
    state.availablePartidaMaterials.splice(index, 1, newData)
  },
  deletePartidaMaterial(state, id) {
    let index = findIndex(state.availablePartidaMaterials, oldData => oldData.id === id)
    state.availablePartidaMaterials.splice(index, 1)
  },
  setSearchedPartidaMaterials(state, resources){
    state.searchedPartidaMaterials = resources
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}