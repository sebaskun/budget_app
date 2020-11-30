import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {

  availableBudgetSubcontracts: [],

}

const getters = {
  getAvailableBudgetSubcontracts: state => state.availableBudgetSubcontracts,
  getFilteredBudgetSubcontract: state => filter => state.availableBudgetSubcontracts.filter(item => item.id==filter),
}

const actions = {
  requestBudgetSubcontracts({ commit }, payload) {
    // console.log('params::', payload)
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/subcontracts`, {params: payload.filter}).then(response => {
        const data = response.body
        // console.log("subcontracts>>>>", data, payload)
        commit('setAvailableBudgetSubcontracts', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  deleteBudgetSubcontract({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.delete(`/budget/api/subcontract_budget/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('deleteBudgetSubcontract', payLoad.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  addBudgetSubcontract({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/subcontract_budget/`, payload).then(response => {
        const data = response.body
        commit('addBudgetSubcontract', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  updateBudgetSubcontract({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/subcontract_budget/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updateBudgetSubcontract', data)
        // dispatch('requestBudgetSubcontracts')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Search partidas Resource
  searchBudgetSubcontracts({ commit }, budgetId, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${budgetId}/subcontracts`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedBudgetSubcontracts', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {

  setAvailableBudgetSubcontracts(state, resources = []) {
    state.availableBudgetSubcontracts = resources
  },

  updateBudgetSubcontract(state, newData) {
    let index = findIndex(state.availableBudgetSubcontracts, oldData => oldData.id === newData.id)
    state.availableBudgetSubcontracts.splice(index, 1, newData)
  },

  deleteBudgetSubcontract(state, id) {
    let index = findIndex(state.availableBudgetSubcontracts, oldData => oldData.id === id)
    state.availableBudgetSubcontracts.splice(index, 1)
  },

  addBudgetSubcontract(state, newData) {
    state.availableBudgetSubcontracts.push(newData)
  },

  // setSearchedPartidaMaterials(state, resources){
  //   state.availableBudgetMaterials = resources
  // },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}