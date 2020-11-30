import Vue from 'vue'

const state = {
  availableCategoryEquipments: [],
  selectedCategoryEquipment: {},
}

const getters = {
  getCategoryEquipments: state => state.availableCategoryEquipments,
  getSelectedCategoryEquipment: state => state.selectedCategoryEquipment,
  getFilteredCategoryEquipments: state => filter => state.availableCategoryEquipments.filter(item => item.padre==filter)
}

const actions = {
  requestCategoryEquipments({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/resource/api/category_equipment/', {params: search})
      .then(response => {
      const data = response.body.results
      // console.log("result Regimen:", data, "params:", search)
      commit('setCategoryEquipments', data)
      resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addCategoryEquipment({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.post('/resource/api/category_equipment/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        // commit('setAvailableListRegimen', data)
        dispatch('requestCategoryEquipments')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateCategoryEquipment({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      //console.log("datos:", payLoad)
      Vue.http.patch(`/resource/api/category_equipment/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        dispatch('requestCategoryEquipments')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  removeCategoryEquipment({ commit, dispatch, state }, payload) {
    return new Promise((resolve, reject) => {
        Vue.http.get(`/resource/api/category_equipment/${payload.id}/delete`).then(response => {
        const data = response
        // commit('setSelectedBudget', data)
        commit('removeCategoryEquipment', payload.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setCategoryEquipments(state, results = []) {
    state.availableCategoryEquipments = results
  },
  removeCategoryEquipment(state, id) {
    let index = findIndex(state.availableCategoryEquipments, oldCategoryEquipment => oldCategoryEquipment.id === id)
    state.availableCategoryEquipments.splice(index, 1)
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}