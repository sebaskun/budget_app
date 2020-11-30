import Vue from 'vue'

const state = {
  availableListRegimen: [],
  selectedRegimen: {},
}

const getters = {
  getAvailableListRegimen: state => state.availableListRegimen,
  getSelectedRegimen: state => state.selectedRegimen,
  getFilteredListCategorias: state => regimen => state.availableListRegimen.filter(item => item.regimen==regimen),
}

const actions = {
  
  requestAvailableListRegimen({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/api/regimen/', {params: search})
      .then(response => {
        const data = response.body.results
        // console.log("result Regimen:", data, "params:", search)
        commit('setAvailableListRegimen', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addRegimen({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      // console.log("datos:", payLoad)
      Vue.http.post('/api/regimen/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        dispatch('requestAvailableListRegimen', {regimen: payLoad.regimen})
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateRegimen({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      // console.log("datos:", payLoad)
      Vue.http.patch(`/api/regimen/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        dispatch('requestAvailableListRegimen', {regimen: payLoad.regimen})
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setAvailableListRegimen(state, results = []) {
    state.availableListRegimen = results
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
