import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableEquipments: [],
  selectedEquipment: {},
}

const getters = {
  getEquipments: state => state.availableEquipments,
  getSelectedEquipment: state => state.selectedEquipment,
  getFilteredEquipments: state => filter => state.availableEquipments.filter(item => item.category==filter)
}

const actions = {
  requestEquipments({ commit }, payload) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/resource/api/equipment/', {params: payload})
      .then(response => {
        const data = response.body.results
        const totalRows = response.data.count
      // console.log("result Regimen:", data, "params:", search)
        commit('setEquipments', data)
        resolve({data, totalRows})
      }).catch(error => {
        reject(error)
      })
    })
  },
  addEquipment({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.post('/resource/api/equipment/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        // commit('setAvailableListRegimen', data)
        dispatch('requestEquipments')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateEquipment({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.patch(`/resource/api/equipment/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        dispatch('requestEquipments')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  removeEquipment({ commit, dispatch, state }, payload) {
    return new Promise((resolve, reject) => {
        Vue.http.get(`/resource/api/equipment/${payload.id}/delete`).then(response => {
        const data = response
        // commit('setSelectedBudget', data)
        commit('removeEquipment', payload.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setEquipments(state, results = []) {
    state.availableEquipments = results
  },
  removeEquipment(state, id) {
    let index = findIndex(state.availableEquipments, oldEquipment => oldEquipment.id === id)
    state.availableEquipments.splice(index, 1)
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}