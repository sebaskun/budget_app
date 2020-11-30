import Vue from 'vue'
import findIndex from 'lodash/findIndex'

const state = {
  availableBudgets: [],
  availableBudgetManpowers: [],
  // availableBudgetMaterials: [],
  availableBudgetSubcontracts: [],
  // availableBudgetEquipments: [],
  availableBudgetPartidas: [],
  selectedBudget: {},
  selectedPartida: {},
  availablePartidaManpowers: [],
  availablePartidaMaterials: [],
  availablePartidaSubcontracts: [],
  availablePartidaEquipments: [],

  searchedPartidaManpowers: [],
  searchedPartidaMaterials: [],
  searchedPartidaSubcontracts: [],
  searchedPartidaEquipments: [],

}

const getters = {
  getSelectedBudget: state => state.selectedBudget,
  getAvailableBudgets: state => state.availableBudgets,
  getAvailableBudgetManpowers: state => state.availableBudgetManpowers,
  // getAvailableBudgetMaterials: state => state.availableBudgetMaterials,
  getAvailableBudgetSubcontracts: state => state.availableBudgetSubcontracts,
  // getAvailableBudgetEquipments: state => state.availableBudgetEquipments,
  getAvailableBudgetPartidas: state => state.availableBudgetPartidas,
  // getFilteredBudgetMaterials: state => filter => state.availableBudgetMaterials.filter(item => item.type_material==filter),
  getFilteredBudgetPartida: state => filter => state.availableBudgetPartidas.filter(item => item.id==filter),

  getAvailablePartidaManpowers: state => state.availablePartidaManpowers,
  getAvailablePartidaMaterials: state => state.availablePartidaMaterials,
  getAvailablePartidaSubcontracts: state => state.availablePartidaSubcontracts,
  getAvailablePartidaEquipments: state => state.availablePartidaEquipments,

  // getSearchedPartidaManpowers: state => search => state.availablePartidaManpowers.filter(item => {
  //   let name = item.get_resource_name
  //   name = name.normalize('NFD').replace(/[\u0300-\u036f]/g, "")
  //   return name == search.normalize('NFD').replace(/[\u0300-\u036f]/g, "")

  // })

  getSearchedPartidaManpowers: state => state.searchedPartidaManpowers,
  getSearchedPartidaMaterials: state => state.searchedPartidaMaterials.filter(item => item.type_material=="S"),
  getSearchedPartidaSubcontracts: state => state.searchedPartidaSubcontracts,
  getSearchedPartidaEquipments: state => state.searchedPartidaEquipments,
}

const actions = {
  requestBudgetPartidas({ commit }, budgetId) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${budgetId}/tasks`).then(response => {
        const data = response.body
        // console.log("partidas>>>>", data)
        commit('setAvailableBudgetPartidas', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // requestBudgetEquipments({ commit }, budgetId, search = {}) {
  //   Vue.http.get(`/budget/api/budgets/${budgetId}/equipments`, {search: search}).then(response => {
  //     commit('setAvailableBudgetEquipments', response.body);
  //   });
  // },
  // requestBudgetMaterials({ commit }, budgetId, search = {}) {
  //   Vue.http.get(`/budget/api/budgets/${budgetId}/materials`, {search: search}).then(response => {
  //     // console.log("data:::>>>>", response.body)
  //     commit('setAvailableBudgetMaterials', response.body);
  //   });
  // },
  requestBudgetSubcontracts({ commit }, budgetId, search = {}) {
    Vue.http.get(`/budget/api/budgets/${budgetId}/subcontracts`, {search: search}).then(response => {
      commit('setAvailableBudgetSubcontracts', response.body);
    });
  },
  requestBudgetManpowers({ commit }, budgetId, search = {}) {
    Vue.http.get(`/budget/api/budgets/${budgetId}/manpowers`, {search: search}).then(response => {
      commit('setAvailableBudgetManpowers', response.body);
    });
  },
  updateBudgetInformation({ commit }, budgetId) {
    Vue.http.get(`budget/api/budgets/${budgetId}/`).then(response => {
      commit('updateBudget', response.body)
    })
  },
  requestBudgetInformation({ commit }, budgetId) {
    Vue.http.get(`budget/api/budgets/${budgetId}/`).then(response => {
     commit('setSelectedBudget', response.body)
    })
  },
  requestBudgets({ commit }, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/`, {search}).then(response => {
        const data = response.body
        // console.log("budget::", data.results)
        commit('setAvailableBudgets', data.results)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },
  addBudget({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/budgets/`, payload).then(response => {
        const data = response.body
        commit('addBudget', data)
        // dispatch('requestBudgets')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateBudget({ commit, dispatch, rootGetters }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/budgets/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('setSelectedBudget', data)
        dispatch('eppBudget/requestEPPs', payload.id, { root: true})
        dispatch('requestBudgetManpowers', payload.id)
        dispatch('requestBudgetPartidas', payload.id)
        dispatch('subcontractBudget/requestBudgetSubcontracts', payload, { root: true})
        let typeMaterial = rootGetters['materialBudget/getCurrentTypeMaterial']
        let paramsMaterial = {
          id: payload.id,
          filter: {type_material: typeMaterial}
        }
        dispatch('materialBudget/requestBudgetMaterials', paramsMaterial, { root: true})
        let categoryEquipment = rootGetters['equipmentBudget/getCurrentCategoryEquipment']
        let paramsEquipment = {
          id: payload.id,
          filter: {category: categoryEquipment}
        }
        dispatch('equipmentBudget/requestBudgetEquipments', paramsEquipment, { root: true})
        commit('updateBudget', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  removeBudget({ commit, dispatch, state }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/delete`).then(response => {
        const data = response
        commit('removeBudget', payload.id)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  addBudgetManpower({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/manpower_budget/`, payload).then(response => {
        const data = response.body
        dispatch('requestBudgetManpowers')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateBudgetManpower({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/manpower_budget/${payload.id}/`, payload).then(response => {
        const data = response.body
        dispatch('requestBudgetManpowers')
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addBudgetPartida({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/tasks/`, payload).then(response => {
        const data = response.body
        dispatch('requestBudgetPartidas', payload.budget)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updateBudgetPartida({ commit, dispatch }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/tasks/${payload.id}/`, payload).then(response => {
        const data = response.body
        dispatch('requestBudgetPartidas', payload.budget)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Search partidas Resource
  searchPartidaManpowers({ commit }, payload, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/manpowers`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedPartidaManpowers', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  searchPartidaMaterials({ commit }, payload, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/materials`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedPartidaMaterials', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  searchPartidaSubcontracts({ commit }, payload, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/subcontracts`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedPartidaSubcontracts', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  searchPartidaEquipments({ commit }, payload, search = {}) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/budgets/${payload.id}/equipments`, {params: search}).then(response => {
        const data = response.body
        commit('setSearchedPartidaEquipments', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },


  // Requests partidas Resource
  requestPartidaManpowers({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/tasks/${payload.id}/manpowers`).then(response => {
        const data = response.body
        commit('setAvailablePartidaManpowers', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  requestPartidaSubcontracts({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/tasks/${payload.id}/subcontracts`).then(response => {
        const data = response.body
        commit('setAvailablePartidaSubcontracts', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  requestPartidaMaterials({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/tasks/${payload.id}/materials`).then(response => {
        const data = response.body
        commit('setAvailablePartidaMaterials', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  requestPartidaEquipments({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.get(`budget/api/tasks/${payload.id}/equipments`).then(response => {
        const data = response.body
        commit('setAvailablePartidaEquipments', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Update Resource Partida
  updatePartidaManpower({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/manpower_task/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updatePartidaManpower', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updatePartidaSubcontract({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/subcontract_task/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updatePartidaSubcontract', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updatePartidaMaterial({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/material_task/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updatePartidaMaterial', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  updatePartidaEquipment({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.patch(`budget/api/equipment_task/${payload.id}/`, payload).then(response => {
        const data = response.body
        commit('updatePartidaEquipment', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // Add Resource Partida
  addPartidaManpower({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/manpower_task/`, payload).then(response => {
        const data = response.body
        commit('addPartidaManpower', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addPartidaSubcontract({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/subcontract_task/`, payload).then(response => {
        const data = response.body
        commit('addPartidaSubcontract', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addPartidaMaterial({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/material_task/`, payload).then(response => {
        const data = response.body
        commit('addPartidaMaterial', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  addPartidaEquipment({ commit }, payload) {
    return new Promise((resolve, reject) => {
      Vue.http.post(`budget/api/equipment_task/`, payload).then(response => {
        const data = response.body
        commit('addPartidaEquipment', data)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
}

const mutations = {
  setAvailableBudgetPartidas(state, partidas = []) {
    state.availableBudgetPartidas = partidas
  },
  setAvailableBudgets(state, budgets = []) {
    state.availableBudgets = budgets
  },
  // setAvailableBudgetEquipments(state, resources = []) {
  //   state.availableBudgetEquipments = resources
  // },
  setAvailableBudgetManpowers(state, resources = []) {
    state.availableBudgetManpowers = resources
  },
  // setAvailableBudgetMaterials(state, resources = []) {
  //   // console.log("resources:_:_:_:", resources)
  //   state.availableBudgetMaterials = resources
  // },
  setAvailableBudgetSubcontracts(state, resources = []) {
    state.availableBudgetSubcontracts = resources
  },
  addBudget(state, newBudget) {
    state.availableBudgets.push(newBudget)
  },
  updateBudget(state, newBudget) {
    let index = findIndex(state.availableBudgets, oldBudget => oldBudget.id === newBudget.id)
    state.availableBudgets.splice(index, 1, newBudget)
  },
  removeBudget(state, id) {
    let index = findIndex(state.availableBudgets, oldBudget => oldBudget.id === id)
    state.availableBudgets.splice(index, 1)
  },
  setSelectedBudget(state, budget){
    state.selectedBudget = budget
  },

  setAvailablePartidaManpowers(state, resources){
    state.availablePartidaManpowers = resources
  },  
  setAvailablePartidaMaterials(state, resources){
    state.availablePartidaMaterials = resources
  },
  setAvailablePartidaSubcontracts(state, resources){
    state.availablePartidaSubcontracts = resources
  },
  setAvailablePartidaEquipments(state, resources){
    state.availablePartidaEquipments = resources
  },

  updatePartidaEquipment(state, newData) {
    let index = findIndex(state.availablePartidaEquipments, oldData => oldData.id === newData.id)
    state.availablePartidaEquipments.splice(index, 1, newData)
  },
  updatePartidaManpower(state, newData) {
    let index = findIndex(state.availablePartidaManpowers, oldData => oldData.id === newData.id)
    state.availablePartidaManpowers.splice(index, 1, newData)
  },
  updatePartidaMaterial(state, newData) {
    let index = findIndex(state.availablePartidaMaterials, oldData => oldData.id === newData.id)
    state.availablePartidaMaterials.splice(index, 1, newData)
  },
  updatePartidaSubcontract(state, newData) {
    let index = findIndex(state.availablePartidaSubcontracts, oldData => oldData.id === newData.id)
    state.availablePartidaSubcontracts.splice(index, 1, newData)
  },

  addPartidaEquipment(state, newData) {
    state.availablePartidaEquipments.push(newData)
  },
  addPartidaManpower(state, newData) {
    state.availablePartidaManpowers.push(newData)
  },
  addPartidaMaterial(state, newData) {
    state.availablePartidaMaterials.push(newData)
  },
  addPartidaSubcontract(state, newData) {
    state.availablePartidaSubcontracts.push(newData)
  },

  setSearchedPartidaEquipments(state, resources){
    state.searchedPartidaEquipments = resources
  },
  setSearchedPartidaMaterials(state, resources){
    state.searchedPartidaMaterials = resources
  },
  setSearchedPartidaManpowers(state, resources){
    state.searchedPartidaManpowers = resources
  },
  setSearchedPartidaSubcontracts(state, resources){
    state.searchedPartidaSubcontracts = resources
  },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}