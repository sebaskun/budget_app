import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableEPPDetails: [],
  selectedEPPDetail: {},
}

const getters = {
  getEPPDetails: state => state.availableEPPDetails,
  getSelectedEPPDetail: state => state.selectedEPPDetail,
  getFilteredEPPDetail: state => filter => state.availableEPPDetails.filter(item => item.epp_budget==filter)
}

const actions = {
  requestEPPDetails({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/budget/api/epp_budget_detail/', {params: search})
      .then(response => {
        const data = response.body.results
        // console.log("result Regimen:", data, "params:", search)
        commit('setEPPDetails', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addEPPDetail({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.post('/budget/api/epp_budget_detail/', payLoad)
      .then(response => {
        const data = response.body
        commit('addEPPDetail', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateEPPDetail({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.patch(`/budget/api/epp_budget_detail/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('updateEPPDetail', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  deleteEPPDetail({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.delete(`/budget/api/epp_budget_detail/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        commit('deleteEPPDetail', payLoad.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  
  setEPPDetails(state, results = []) {
    state.availableEPPDetails = results
  },

  updateEPPDetail(state, newData) {
    let index = findIndex(state.availableEPPDetails, oldData => oldData.id === newData.id)
    state.availableEPPDetails.splice(index, 1, newData)
  },

  deleteEPPDetail(state, id) {
    let index = findIndex(state.availableEPPDetails, oldData => oldData.id === id)
    state.availableEPPDetails.splice(index, 1)
  },

  addEPPDetail(state, newData) {
    state.availableEPPDetails.push(newData)
  },

}

export default {
  // namespaced: true,
  state,
  getters,
  actions,
  mutations
}