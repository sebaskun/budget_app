import Vue from 'vue'

const state = {
  availableListCertificado: [],
  selectedCertificado: {},
}

const getters = {
  getAvailableListCertificado: state => state.availableListCertificado,
  getSelectedCertificado: state => state.selectedCertificado,
  getFilteredCertificado: state => filter => state.availableListCertificado.filter(item => item.id==filter)
}

const actions = {
  requestAvailableListCertificado({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/api/certificado/', {params: search})
      .then(response => {
        const data = response.body.results
        // console.log("result Regimen:", data, "params:", search)
        commit('setAvailableListCertificado', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addCertificado({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.post('/api/certificado/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        // commit('setAvailableListRegimen', data)
        dispatch('requestAvailableListCertificado')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateCertificado({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.patch(`/api/certificado/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        dispatch('requestAvailableListCertificado')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setAvailableListCertificado(state, results = []) {
    state.availableListCertificado = results
  }
}

export default {
  // namespaced: true,
  state,
  getters,
  actions,
  mutations
}
