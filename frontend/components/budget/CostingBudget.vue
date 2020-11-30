<template>
  <b-row>
    <b-col md="10">
      <app-title :title="budget.code + ' - ' + budget.title"
        subTitle="Resumen">
        <template slot="options">
            <b-button size="sm" @click="showImportForm=true">Importar actividades...</b-button>
            <b-button size="sm" @click="onEditTree">Modificar...</b-button>
        </template>
      </app-title>

      <b-row class="bd-content">
        <b-col md=12 class="my-1">
          <div class="nested">
          <div class="navigation-filter">
            <input type="text" v-model="treeFilter" placeholder="Escriba lo que desea filtrar...">
          </div>

          <tree
            :data="data"
            :options="treeOptions"
            :filter="treeFilter"
            ref="tree"
            v-model="selectedNode">
            <div class="container-row" slot-scope="{ node }">
              <div class="row">
                <div class="col col-400">
                  <router-link
                    :to="{ name:'budget-apu', params: {budget: budget.id, task: node.data.id} }">
                    <template v-if="hasChildren(node)"><span style="color: red;">{{ node.text }}</span></template>
                    <template v-else>{{ node.text }}</template>
                  </router-link>
                </div>
                <div class="col-sm col-50">
                  <template v-if="!hasChildren(node)">{{ node.data.unit }}</template>
                </div>
                <div class="col-sm text-right col-100">
                  <template v-if="!hasChildren(node)">{{ node.data.quantity|decimal("0.00") }}</template>
                </div>
                <div class="col-sm text-right col-100">
                  <template v-if="!hasChildren(node)">{{ node.data.unit_subtotal|currency(budget.currency) }}</template>
                </div>
                <div class="col-sm text-right col-100">
                  {{ node.data.subtotal|currency(budget.currency) }}
                </div>

                <div>
                  <b-dropdown variant="link" size="lg" no-caret>
                    <template slot="button-content">
                      &#x2630;<span class="sr-only">Opciones</span>
                    </template>
                    <b-dropdown-item @mouseup.stop="nuevo(node)" href="#">Adicionar</b-dropdown-item>
                    <b-dropdown-item @mouseup.stop="copiar(node)" href="#">Copiar</b-dropdown-item>
                    <b-dropdown-item @mouseup.stop="eliminar(node)" href="#">Eliminar...</b-dropdown-item>
                  </b-dropdown>
                </div>
              </div>

            </div>

          </tree>
          </div>
        </b-col>
      </b-row>

    </b-col>
    <b-col md="2">
      <app-menu/>
    </b-col>
  </b-row>
</template>

<script>
  import ImportTask from "./task/ImportTask.vue"
  import Menu from "./nav/Menu.vue"
  import { mapGetters } from 'vuex'
  import Title from "../utils/Title.vue"
  import LiquorTree from 'liquor-tree'
  import buildTree from '../../utils/tree'

  const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }

  var numeral = require('numeral')
  const url_api = `/budget/api/budgets/`
  export default {
      components: {
          'app-import-task': ImportTask,
          'app-menu': Menu,
          'app-title': Title,
          [LiquorTree.name]: LiquorTree
      },
      data() {
        return {
          selectedNode: null,
          treeFilter: "",
          showAPU: false,
          tasks: [],
          tree: [],
          lenTasks: 0,
          // budget: {},
          budgetId: "",
          showImportForm: false,
          filter: null,
          progress: 0,
          count: 0,
          node: "",
          title: "",
          typeResource: "",
          editTree: false,
          treeOptions: {
            // propertyNames: {
            //   text: 'name',
            // },
            dnd: true,
            // fetchData(node) {
            //   console.log("se leyó:::", node)
            //   return this.$http.get(`/budget/api/tasks/${node.data.id}/`)
            // },
          },
          // data: this.getTasks(this.$route.params.budget)
          data: null
        }
      },
      created() {
        // this.budgetId = this.$route.params.budget
        // this.getBudget()
        // console.log("::created::", this.budgetId)
        this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
      },
      watch: {
        '$route'(to, from){
          // this.budgetId = this.$route.params.budget
          // this.getBudget()
          this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
          this.data = this.getTasks()
          this.$refs.tree.setModel(this.data)
        },
        budget(){
          // console.log("cambio el budget")
          this.data = this.getTasks()
          this.$refs.tree.setModel(this.data)
        }
      },
      computed: {
        // ...mapGetters({
        //     budgets: 'getAvailableBudgets',
        // }),
        budget(){
          return this.$store.getters['budget/getSelectedBudget']
        },
      },
      // mounted() {
      //   // this.$refs.tree.$on("node:dragging:finish", this.onSaveBudget({tree: this.$refs.tree.tree.model}))
      //   this.$refs.tree.$on("node:dragging:finish", ()=>{
      //     // console.log("tree---->", this.$refs.tree.tree )
      //     this.onSaveBudget({tree: this.$refs.tree.tree.model})
      //   })
      // },
      methods: {
        nuevo(node){
          const url = `budget/api/tasks/`
          this.$http.post(url, {name: "Nueva actividad sin nombre.", wbs:0, budget: this.budget.id})
            .then((response) => {
              node.after({
                text: response.body.name,
                id: response.body.id,
                data: {
                  id: response.body.id,
                }
              })
              this.onSaveBudget({tree: this.$refs.tree.tree.model})
              this.$swal({
                position: 'top-end',
                toast: true,
                type: 'success',
                title: 'Se creó una nueva actividad correctamente.',
                showConfirmButton: false,
                timer: 1500
              })
            })
            .catch((err)=> {
              var msgError = ""
              Object.getOwnPropertyNames(err.body).forEach((element) => {
                msgError += `${element} : ${err.body[element]}\n`
              })
              this.$swal({
                type: 'error',
                title: 'Oops...',
                text: 'Error, no se pudo crear nueva actividad\n' + msgError
              })
            }
            )
        },
        copiar(node){
          // console.log("copiar:::", node)
          const url = `/budget/api/tasks/${node.data.id}/copy/`
          this.$http.get(url)
            .then((response) => {

              node.after({
                text: response.body.name,
                id: response.body.id,
                data: {
                  id: response.body.id,
                  quantity: response.body.quantity,
                  subtotal: response.body.get_subtotal,
                  unit: response.body.unit,
                  unit_subtotal: response.body.get_unit_subtotal,
                  text: response.body.name,
                }
              })
              this.onSaveBudget({tree: this.$refs.tree.tree.model})
              this.$swal({
                position: 'top-end',
                toast: true,
                type: 'success',
                title: 'Se copió correctamente.',
                showConfirmButton: false,
                timer: 1500
              })
            })
            .catch((err)=> {
              var msgError = ""
              Object.getOwnPropertyNames(err.body).forEach((element) => {
                msgError += `${element} : ${err.body[element]}\n`
              })
              this.$swal({
                type: 'error',
                title: 'Oops...',
                text: 'Error, no se pudo hacer una copia\n' + msgError
              })
            }
            )
        },
        eliminar(node){
          console.log("eliminar:::", node)
          const url = `/budget/api/tasks/${node.data.id}/`
          this.$swal({
            title: "¿Está seguro de eliminar la tarea?",
            text: "Una vez eliminado no se podrá recuperar!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminar!'
          })
          .then((willDelete) => {
            if (willDelete.value) {
              this.$http.delete(url)
                .then((response)=>{
                  node.remove()
                  this.onSaveBudget({tree: this.$refs.tree.tree.model})
                  this.$swal({
                    position: 'top-end',
                    toast: true,
                    type: 'success',
                    title: 'Se eliminó correctamente.',
                    showConfirmButton: false,
                    timer: 1500
                  })
                })
                .catch((err)=> {
                  var msgError = ""
                  Object.getOwnPropertyNames(err.body).forEach((element) => {
                    msgError += `${element} : ${err.body[element]}\n`
                  })
                  this.$swal({
                    type: 'error',
                    title: 'Oops...',
                    text: 'Error, no se pudo eliminar\n' + msgError
                  })
                })
            }
          })
        },
        hasChildren(node){
          const hasChildren = node.children && node.children.length
          if(hasChildren){
            let total = 0
            node.children.forEach((item)=>{
              if(item.data.subtotal!==undefined){
              total += parseFloat(item.data.subtotal)
              // console.log("Item:::", item.data.subtotal)
              }
            })
            this.$set(node.data, "subtotal", total)
            // console.log("total::", node.data.subtotal)
          }
          return hasChildren
        },
        onSaveBudget(data) {
          // console.log("Guardado:::", JSON.stringify(data))
          // console.log("Guardado:::", data)

          let url = `/budget/api/budgets/${this.budget.id}/`
          let vm = this
          this.$http.patch(url, data)
            .then((response) => {
              this.$swal({
                position: 'top-end',
                toast: true,
                type: 'success',
                title: 'Se guardó correctamente.',
                showConfirmButton: false,
                timer: 1500
              })
              // vm.$store.dispatch('requestTaskInformation', vm.task.id)
              // this.getBudget()
            })
            .catch((err) => {
              var msgError = ""
              Object.getOwnPropertyNames(err.body).forEach((element) => {
                msgError += `${element} : ${err.body[element]}\n`
              });
              this.$swal({
                type: 'error',
                title: 'Oops...',
                text: 'Error, no se pudo guardar\n' + msgError
              })
            })
        },
        // getBudget(){
        //   let url = `${url_api}${this.budgetId}/`
        //   this.$http.get(url)
        //     .then((response) => {
        //       this.budget = response.data
        //     })
        //     .catch((err) => {
        //       console.log("error en getBudget", err)
        //     })
        // },
        // getTasks(){
        //   console.log("tree:::::", this.budget.tree)
        //   return new Promise((resolve, reject)=>{
        //     resolve(this.budget.tree)
        //   })
        // },
        // getTasks(budgetId){
        //   return new Promise((resolve, reject) => {
        //     this.$http.get(`/budget/api/budgets/${budgetId}/tasks/`)
        //   .then(response => {
        //     var tree;
        //     // tree = buildTree(response.data)
        //     if(this.budget.tree){
        //       tree = this.budget.tree
        //     }else{
        //       tree = buildTree(response.data)
        //       this.onSaveBudget({tree: tree})
        //     }
        //     // console.log("tree:", tree)
        //     resolve(tree)
        //   })
        //   .catch(error => {
        //     reject(error)
        //   })
        // })
        // },
        getTasks(){
          if(this.budget){
            return this.budget.tree
          }else{
            return null
          }
        },
        onEditTree(){
          this.editTree = !this.editTree
          this.$store.dispatch('setEditTree', this.editTree)
        },
        addTask(task){
          let url = `/budget/api/tasks/`
          this.$http.post(url, task)
            .then((response) => {
              this.count += 1
              this.progress = (this.count * 100 / this.lenTasks).toFixed(2)
            })
            .catch((err) => {
              console.log('error: ', err, task);
            })
        },
        onTaskAPU(node){
          this.node = node
          this.showAPU = true
        },
        closeResourceBudget(){
          this.typeResource = ""
        },
        closeApuTask(){
          this.showAPU
        },
        bulkTasks(tasks, deleteTasks){
          this.showImportForm = false
          if (deleteTasks){
            // Borramos todas las tareas de este budget
              this.$http.get(`/budget/api/budgets/${this.budgetId}/tasks/delete`)
                .then((response) => {
                  // Guardamos todas las tareas a la base de datos
                  let lenTasks = tasks.length
                  for (var index in tasks){
                    this.addTask(tasks[index])
                    // console.log("task:", tasks[index])
                  }
                  // Cargamos todas las tareas
                  this.$store.dispatch('getTaskListByBudget', value)
                  // this.getTasks()
                  // console.log("Se importaron todas las tareas")
                })
                .catch((err) => {
                  console.log(err);
                });
          }
        }
      }
  }
</script>
