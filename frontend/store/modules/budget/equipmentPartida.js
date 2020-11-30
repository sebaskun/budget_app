import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availablePartidaEquipments: [],
  searchedPartidaEquipments: [],
}

const getters = {
  getAvailablePartidaEquipments: state => state.availablePartidaEquipments,
  getSearchedPartidaEquipments: state => state.searchedPartidaEquipments,
}

const actions = {
  // Search partidas Resource
  searchPartidaEquipments({ commit }, payload, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/equipments`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedPartidaEquipments', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Requests partidas Resource
  requestPartidaEquipments({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/tasks/${payload.id}/equipments`).then(response => {
        const data = response.body
        commit('setAvailablePartidaEquipments', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Update Resource Partida
  updatePartidaEquipment({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/equipment_task/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updatePartidaEquipment', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Add Resource Partida
  addPartidaEquipment({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/equipment_task/`, payload).then(response => {
        const data = response.body
        commit('addPartidaEquipment', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Delete Resource Partida
  deletePartidaEquipment({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.delete(`budget/api/equipment_task/${payload.id}/`).then(response => {
        const data = response.body
        commit('deletePartidaEquipment', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}
const mutations = {
  setAvailablePartidaEquipments(state, resources){
    state.availablePartidaEquipments = resources
  },
  addPartidaEquipment(state, newData) {
    state.availablePartidaEquipments.push(newData)
  },
  updatePartidaEquipment(state, newData) {
    let index = findIndex(state.availablePartidaEquipments, oldData => oldData.id === newData.id)
    state.availablePartidaEquipments.splice(index, 1, newData)
  },
  deletePartidaEquipment(state, id) {
    let index = findIndex(state.availablePartidaEquipments, oldData => oldData.id === id)
    state.availablePartidaEquipments.splice(index, 1)
  },
  setSearchedPartidaEquipments(state, resources){
    state.searchedPartidaEquipments = resources
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}