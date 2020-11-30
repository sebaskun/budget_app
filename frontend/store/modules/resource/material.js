import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableMaterials: [],
  selectedMaterial: {},
}

const getters = {
  getMaterials: state => state.availableMaterials,
  getSelectedMaterial: state => state.selectedMaterial,
  getFilteredMaterials: state => filter => state.availableMaterials.filter(item => item.class_cost==filter)
}

const actions = {
  requestMaterials({ commit }, payload) {
    // console.log("params>>>", payload)
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/resource/api/material/', {params: payload})
      .then(response => {
        const data = response.body.results
        const totalRows = response.data.count
        // console.log("result Regimen:", data, "params:", search)
        commit('setMaterials', data)
        resolve({data, totalRows})
      }).catch(error => {
        reject(error)
      })
    })
  },
  addMaterial({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.post('/resource/api/material/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        // commit('setAvailableListRegimen', data)
        dispatch('requestMaterials')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateMaterial({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.patch(`/resource/api/material/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        dispatch('requestMaterials')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  removeMaterial({ commit, dispatch, state }, payload) {
    return new Promise((resolve, reject) => {
        Vue.http.get(`/resource/api/material/${payload.id}/delete`).then(response => {
        const data = response
        // commit('setSelectedBudget', data)
        commit('removeMaterial', payload.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setMaterials(state, results = []) {
    state.availableMaterials = results
  },
  removeMaterial(state, id) {
    let index = findIndex(state.availableMaterials, oldMaterial => oldMaterial.id === id)
    state.availableMaterials.splice(index, 1)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}