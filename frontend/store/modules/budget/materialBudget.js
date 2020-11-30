import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {

  availableBudgetMaterials: [],
  currentTypeMaterial: null,

}

const getters = {
  getAvailableBudgetMaterials: state => state.availableBudgetMaterials,
  getFilteredBudgetMaterials: state => filter => state.availableBudgetMaterials.filter(item => item.type_material==filter),
  getCurrentTypeMaterial: state=> state.currentTypeMaterial
}

const actions = {
  setTypeMaterial ({commit}, payload){
    commit('setTypeMaterial', payload)
    // state.currentTypeMaterial = payload
  },

  requestBudgetMaterials({ commit }, payload) {
    // console.log('params::', payload)
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/materials`, {params: payload.filter}).then(response => {
        const data = response.body
        // console.log("materials>>>>", data, payload)
        commit('setAvailableBudgetMaterials', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  deleteBudgetMaterial({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.delete(`/budget/api/material_budget/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('deleteBudgetMaterial', payLoad.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  addBudgetMaterial({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/material_budget/`, payload).then(response => {
        const data = response.body
        commit('addBudgetMaterial', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  updateBudgetMaterial({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/material_budget/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updateBudgetMaterial', data)
        // dispatch('requestBudgetMaterials')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Search partidas Resource
  searchBudgetMaterials({ commit }, budgetId, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${budgetId}/materials`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedBudgetMaterials', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {

  setTypeMaterial(state, value){
    state.currentTypeMaterial = value
  },

  setAvailableBudgetMaterials(state, resources = []) {
    state.availableBudgetMaterials = resources
  },

  updateBudgetMaterial(state, newData) {
    let index = findIndex(state.availableBudgetMaterials, oldData => oldData.id === newData.id)
    state.availableBudgetMaterials.splice(index, 1, newData)
  },

  deleteBudgetMaterial(state, id) {
    let index = findIndex(state.availableBudgetMaterials, oldData => oldData.id === id)
    state.availableBudgetMaterials.splice(index, 1)
  },

  addBudgetMaterial(state, newData) {
    state.availableBudgetMaterials.push(newData)
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