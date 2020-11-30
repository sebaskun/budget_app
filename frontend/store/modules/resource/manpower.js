import Vue from 'vue'

const state = {
  availableManpowers: [],
  selectedManpower: {},
  resultManpowers: []
}

const getters = {
  getManpowers: state => state.availableManpowers,
  getSelectedManpower: state => state.selectedManpower,
  // getResultManpower: state => state.resultManpowers,
  getFilteredManpower: state => filter => state.availableManpowers.filter(item => item.id==filter)
}

const actions = {
  requestManpowers({ commit, dispatch }, search = {}) {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get('/resource/api/manpower/', {params: search})
      .then(response => {
        const data = response.body.results
        // console.log("result Regimen:", data, "params:", search)
        commit('setManpowers', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  searchManpowers({ commit }, search = "") {
    return new Promise((resolve, reject) => {
      // console.log("search:", search)
      Vue.http.get(`resource/api/manpower/?search=${search}`)
      .then(response => {
        const data = response.body.results
        console.log("Manpowers:", data, "params:", search)
        // commit('setResultManpowers', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addManpower({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.post('/resource/api/manpower/', payLoad)
      .then(response => {
        const data = response.body
        // console.log("addRegimen:", data)
        // commit('setAvailableListRegimen', data)
        dispatch('requestManpowers')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateManpower({ commit, dispatch }, payLoad) {
    return new Promise((resolve, reject) => {
      console.log("datos:", payLoad)
      Vue.http.patch(`/resource/api/manpower/${payLoad.id}/`, payLoad)
      .then(response => {
        const data = response.body
        dispatch('requestManpowers')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setManpowers(state, results = []) {
    state.availableManpowers = results
  },
  // setResultManpowers(state, results = []) {
  //   state.resultManpowers = results
  // }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}