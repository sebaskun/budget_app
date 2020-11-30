import Vue from 'vue'

const state = {
  availableListGrupo: [],
  selectedGrupo: {},
}

const getters = {
  getAvailableListGrupo: state => state.availableListGrupo,
  getSelectedGrupo: state => filter => state.availableListGrupo.filter(item => item.id==filter),
  getFilteredGrupo: state => filter => state.availableListGrupo.filter(item => item.grupo==filter)
}

const actions = {
  requestAvailableListGrupo({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/api/grupos_varios/', {params: search})
      .then(response => {
        const data = response.body.results
        // console.log("result:", data)
        commit('setAvailableListGrupo', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addGrupo({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.post('/api/grupos_varios/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addGrupo:", data)
        dispatch('requestAvailableListGrupo', {grupo: payLoad.grupo})
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateGrupo({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.patch(`/api/grupos_varios/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        // console.log("addGrupo:", data)
        dispatch('requestAvailableListGrupo', {grupo: payLoad.grupo})
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setAvailableListGrupo(state, results = []) {
    state.availableListGrupo = results
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
