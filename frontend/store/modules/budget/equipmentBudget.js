import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {

  availableBudgetEquipments: [],
  currentCategoryEquipment: null,
}

const getters = {
  getAvailableBudgetEquipments: state => state.availableBudgetEquipments,
  getFilteredBudgetEquipments: state => filter => state.availableBudgetEquipments.filter(item => item.category==filter),
  getCurrentCategoryEquipment: state => state.currentCategoryEquipment
}

const actions = {
  setCategoryEquipment ({commit}, payload){
    commit('setCategoryEquipment', payload)
  },

  requestBudgetEquipments({ commit }, payload) {
    // console.log('params::', payload)
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/equipments`, {params: payload.filter}).then(response => {
        const data = response.body
        // console.log("equipments>>>>", data, payload)
        commit('setAvailableBudgetEquipments', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  deleteBudgetEquipment({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.delete(`/budget/api/equipment_budget/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('deleteBudgetEquipment', payLoad.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  addBudgetEquipment({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/equipment_budget/`, payload).then(response => {
        const data = response.body
        commit('addBudgetEquipment', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  updateBudgetEquipment({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/equipment_budget/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updateBudgetEquipment', data)
        // dispatch('requestBudgetEquipments')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Search partidas Resource
  searchBudgetEquipments({ commit }, budgetId, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${budgetId}/equipments`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedBudgetEquipments', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {

  setCategoryEquipment(state, value){
    state.currentCategoryEquipment = value
  },

  setAvailableBudgetEquipments(state, resources = []) {
    state.availableBudgetEquipments = resources
  },

  updateBudgetEquipment(state, newData) {
    let index = findIndex(state.availableBudgetEquipments, oldData => oldData.id === newData.id)
    state.availableBudgetEquipments.splice(index, 1, newData)
  },

  deleteBudgetEquipment(state, id) {
    let index = findIndex(state.availableBudgetEquipments, oldData => oldData.id === id)
    state.availableBudgetEquipments.splice(index, 1)
  },

  addBudgetEquipment(state, newData) {
    state.availableBudgetEquipments.push(newData)
  },

  // setSearchedPartidaEquipments(state, resources){
  //   state.availableBudgetEquipments = resources
  // },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}