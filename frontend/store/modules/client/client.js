import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableClients: [],
  selectedClient: {},
}
const url = 'client/api/clients'

const getters = {
  getSelectedClient: state => state.selectedClient,
  getAvailableClients: state => state.availableClients,
}

const actions = {
    updateClient({ commit }, payload) {
        return new Promise((resolve, reject) => {
            Vue.http.patch(`${url}/${payload.id}/`).then(response => {
                commit('setSelectedClient', response.body)
                resolve()
            }).catch(error => {
                reject(error)
            })
        })
    },
    requestClient({ commit }, payload) {
        return new Promise((resolve, reject) => {
            Vue.http.get(`${url}/${payload.id}/`)
            .then(response => {
                commit('setSelectedClient', response.body)
                resolve()
            })
            .catch(error => {
                reject(error)
            })
        })
    },
    requestClients({ commit }, payload) {
        return new Promise((resolve, reject) => {
            Vue.http.get(`${url}/`, {payload}).then(response => {
                const data = response.body
                commit('setAvailableClients', data.results)
                resolve()
            }).catch(error => {
                reject(error)
            })
        })
    }
}

const mutations = {
  setAvailableClients(state, data = []) {
    state.availableClients = data
  },
  setSelectedClient(state, data){
    state.selectedClient = data
  },
  // setAvailableBudgetEquipments(state, resources = []) {
  //   state.availableBudgetEquipments = resources
  // },
  // setAvailableBudgetManpowers(state, resources = []) {
  //   state.availableBudgetManpowers = resources
  // },
  // setAvailableBudgetMaterials(state, resources = []) {
  //   console.log("resources:_:_:_:", resources)
  //   state.availableBudgetMaterials = resources
  // },
  // setAvailableBudgetSubcontracts(state, resources = []) {
  //   state.availableBudgetSubcontracts = resources
  // },
  // updateBudget(state, newBudget) {
  //   let index = findIndex(state.availableBudgets.results, oldBudget => oldBudget.id === newBudget.id)
  //   state.availableBudgets.results.splice(index, 1, newBudget)
  // },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
