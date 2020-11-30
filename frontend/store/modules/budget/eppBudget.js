import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableEPPs: [],
  selectedEPP: {},
}

const getters = {
  getEPPs: state => state.availableEPPs,
  getSelectedEPP: state => state.selectedEPP,
  getFilteredEPP: state => filter => state.availableEPPs.filter(item => item.budget==filter)
}

const actions = {
  requestEPPs({ commit }, budgetId) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get(`/budget/api/budgets/${budgetId}/epps/`)
      .then(response => {
        const data = response.body
        commit('setEPPs', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addEPP({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.post('/budget/api/epp_budget/', payLoad)
      .then(response => {
        const data = response.body
        commit('addEPP', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateEPP({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.patch(`/budget/api/epp_budget/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('updateEPP', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  deleteEPP({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.delete(`/budget/api/epp_budget/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('deleteEPP', payLoad.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setEPPs(state, results = []) {
    state.availableEPPs = results
  },

  updateEPP(state, newData) {
    let index = findIndex(state.availableEPPs, oldData => oldData.id === newData.id)
    state.availableEPPs.splice(index, 1, newData)
  },

  deleteEPP(state, id) {
    let index = findIndex(state.availableEPPs, oldData => oldData.id === id)
    state.availableEPPs.splice(index, 1)
  },

  addEPP(state, newData) {
    state.availableEPPs.push(newData)
  },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}