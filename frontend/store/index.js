import Vue from 'vue'
import Vuex from 'vuex'
import buildTree from '../utils/tree'
import findIndex from 'lodash/findIndex'
import grupo from './modules/generales/grupo'
import regimen from './modules/generales/regimen'
import certificado from './modules/generales/certificado'
import vacuna from './modules/resource/vacuna'
import vacunaDetail from './modules/resource/vacunaDetail'
import material from './modules/resource/material'
import equipment from './modules/resource/equipment'
import manpower from './modules/resource/manpower'
import subcontract from './modules/resource/subcontract'
import categoryEquipment from './modules/resource/categoryEquipment'
import budget from './modules/budget/budget'
import client from './modules/client/client'
import certificacionBudget from './modules/budget/certificacionBudget'
import eppBudget from './modules/budget/eppBudget'
import eppBudgetDetail from './modules/budget/eppBudgetDetail'
import materialBudget from './modules/budget/materialBudget'
import manpowerBudget from './modules/budget/manpowerBudget'
import equipmentBudget from './modules/budget/equipmentBudget'
import subcontractBudget from './modules/budget/subcontractBudget'
import materialPartida from './modules/budget/materialPartida'
import manpowerPartida from './modules/budget/manpowerPartida'
import equipmentPartida from './modules/budget/equipmentPartida'
import subcontractPartida from './modules/budget/subcontractPartida'

Vue.use(Vuex)

const varios = {
    // namespaced: true,
    state: {
      availableClients: [],
      availableTasks: [],
      availableOverHeads: [],
      selectedTask: {},
      editingTree: false,
      currentTask: {}
    },
    getters: {
      // getSelectedBudget: state => state.selectedBudget,
      getSelectedTask: state => state.selectedTask,
      getAvailableTasks: state => state.availableTasks,
      getAvailableClients: state => state.availableClients,
      getEditingTree: state => state.editingTree,
      getAvailableOverHeads: state => state.availableOverHeads,
      getCurrentTask: state => state.currentTask
    },
    actions: {
      setEditTree({ commit }, value){
        commit('setEditTree', value)
      },


      getTaskListByBudget({ commit }, budgetId) {
        return new Promise((resolve, reject) => {
          Vue.http.get(`/budget/api/budgets/${budgetId}/tasks/`).then(response => {
            let tree = buildTree(response.data)
            commit('setAvailableTasks', tree)
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },


      requestClientList({ commit }, search = {}) {
        Vue.http.get('client/api/clients/', {search: search}).then(response => {
          commit('setAvailableClients', response.body);
        });
      },

      requestTaskInformation({ commit }, taskId) {
        Vue.http.get(`budget/api/tasks/${taskId}/`).then(response => {
          commit('setSelectedTask', response.body)
        })
      },
      updateTaskInformation({ commit, state, dispatch }, taskId) {
        // Update Task by Id
        // console.log("::updateTaskInformation:::", state.availableTasks)
        if(Boolean(state.availableTasks) && Boolean(state.availableTasks.results)){
          Vue.http.get(`budget/api/tasks/${taskId}/`).then(response => {
            console.log("cambio....****")
            commit('updateTask', response.body)
          })
        }
      }
    },
    mutations: {
      setEditTree(state, value){
        state.editingTree = value
      },
      setAvailableBudgets(state, budgets = []) {
        state.availableBudgets = budgets
      },
      setAvailableBudgetEquipments(state, resources = []) {
        state.availableBudgetEquipments = resources
      },
      setAvailableBudgetManpowers(state, resources = []) {
        state.availableBudgetManpowers = resources
      },
      setAvailableBudgetMaterials(state, resources = []) {
        state.availableBudgetMaterials = resources
      },
      setAvailableBudgetSubcontracts(state, resources = []) {
        state.availableBudgetSubcontracts = resources
      },
      setAvailableTasks(state, tasks = []) {
        state.availableTasks = tasks
      },
      updateBudget(state, newBudget) {
        let index = findIndex(state.availableBudgets.results, oldBudget => oldBudget.id === newBudget.id)
        state.availableBudgets.results.splice(index, 1, newBudget)
      },
      updateTask(state, newTask) {
        let index = findIndex(state.availableTasks.results, oldTask => oldTask.id === newTask.id)
        state.availableTasks.results.splice(index, 1, newTask)
      },
      setAvailableClients(state, clients = []){
        state.availableClients = clients
      },
      // setSelectedBudget(state, budget){
      //   state.selectedBudget = budget
      // },
      setSelectedTask(state, task){
        state.selectedTask = task
      },
      overheadSetTotal(state, newValue = {}){
        state.overheadTotal = newValue.number || 0
        return state.overheadTotal
      },
      overheadSetTotalManpower(state, newValue = {}){
        state.overheadTotalManpower = newValue.number || 0
        return state.overheadTotalManpower
      },
      overheadSetTotalStandby(state, newValue = {}){
        state.overheadTotalStandby = newValue.number || 0
        return state.overheadTotalStandby
      },
      overheadSetTotalWorkshop(state, newValue = {}){
        state.overheadTotalWorkshop = newValue.number || 0
        return state.overheadTotalWorkshop
      },
      overheadSetTotalMedical(state, newValue = {}){
        state.overheadTotalMedical = newValue.number || 0
        return state.overheadTotalMedical
      },
      overheadSetTotalOperative(state, newValue = {}){
        state.overheadTotalOperative = newValue.number || 0
        return state.overheadTotalOperative
      },
      overheadSetTotalVarious(state, newValue = {}){
        state.overheadTotalVarious = newValue.number || 0
        return state.overheadTotalVarious
      }
    }
  }

export default new Vuex.Store({
    modules: {
      budget,
      varios,
      grupo,
      regimen,
      certificado,
      client,
      vacuna,
      vacunaDetail,
      certificacionBudget,
      eppBudget,
      eppBudgetDetail,
      material,
      manpower,
      equipment,
      subcontract,
      categoryEquipment,
      materialBudget,
      manpowerBudget,
      equipmentBudget,
      subcontractBudget,
      materialPartida,
      manpowerPartida,
      subcontractPartida,
      equipmentPartida
    },
    namespaced: true,
  }
)


