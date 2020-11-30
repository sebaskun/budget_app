import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {

  availableBudgetManpowers: [],

}

const getters = {
  getAvailableBudgetManpowers: state => state.availableBudgetManpowers,
  getFilteredBudgetManpowers: state => filter => state.availableBudgetManpowers.filter(item => item.type_manpower==filter),
}

const actions = {
  requestBudgetManpowers({ commit }, payload) {
    // console.log('params::', payload)
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/manpowers`, {params: payload.filter}).then(response => {
        const data = response.body
        // console.log("manpowers>>>>", data, payload)
        commit('setAvailableBudgetManpowers', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  deleteBudgetManpower({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.delete(`/budget/api/manpower_budget/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('deleteBudgetManpower', payLoad.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  addBudgetManpower({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/manpower_budget/`, payload).then(response => {
        const data = response.body
        commit('addBudgetManpower', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  updateBudgetManpower({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/manpower_budget/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updateBudgetManpower', data)
        // dispatch('requestBudgetManpowers')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Search partidas Resource
  searchBudgetManpowers({ commit }, budgetId, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${budgetId}/manpowers`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedBudgetManpowers', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {

  setAvailableBudgetManpowers(state, resources = []) {
    state.availableBudgetManpowers = resources
  },

  updateBudgetManpower(state, newData) {
    let index = findIndex(state.availableBudgetManpowers, oldData => oldData.id === newData.id)
    state.availableBudgetManpowers.splice(index, 1, newData)
  },

  deleteBudgetManpower(state, id) {
    let index = findIndex(state.availableBudgetManpowers, oldData => oldData.id === id)
    state.availableBudgetManpowers.splice(index, 1)
  },

  addBudgetManpower(state, newData) {
    state.availableBudgetManpowers.push(newData)
  },

  // setSearchedPartidaManpowers(state, resources){
  //   state.availableBudgetManpowers = resources
  // },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}