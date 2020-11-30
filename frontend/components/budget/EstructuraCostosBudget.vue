<template>
  <b-row>
    <app-title :title="budget.code + ' - ' + budget.title"
        subTitle="Estructura de Costos">
      <template slot="options">
          <b-button size="sm" @click="refresh" >Refrescar</b-button>
          <!-- <b-dropdown size="sm" id="dropdown-1" text ="Versión" class="m-md-2">
          <b-dropdown-item>1</b-dropdown-item>
          <b-dropdown-item>2</b-dropdown-item>
          <b-dropdown-item>3</b-dropdown-item>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item disabled>Nueva versión</b-dropdown-item>
          </b-dropdown> -->
      </template>
    </app-title>
      <b-col md="12" class="my-1">
    <b-row class="bd-content">
      <b-col md="12">
        <div class="navigation-filter">
          <input type="text" v-model="treeFilter" placeholder="Escriba lo que desea filtrar...">
        </div>
      </b-col>
      <b-col md="12">
        <loading :active.sync="isLoading" 
          :is-full-page="fullPage">
        </loading>
        <div class="container-row">
          <div class="row">
            <div class="col col-400">
              Partida
            </div>
            <div class="col-sm text-right col-100">
              Mano Obra
            </div>
            <div class="col-sm text-right col-100">
              Material
            </div>
            <div class="col-sm text-right col-100">
              Subcontrato
            </div>
            <div class="col-sm text-right col-100">
              Equipo
            </div>
            <div class="col-sm text-right col-100">
              TOTAL
            </div>

            <div class="col-sm text-right col-50">

            </div>
          </div>

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
                  <span :class="{'node-parent': hasChildren(node)}">{{ getPartida(node)?getPartida(node).name:"-" }}</span>
                </router-link>
              </div>
              <div class="col-sm text-right col-100">
                <template v-if="hasChildren(node)"><span class="node-parent">{{node.data.subtotal_manpower|currency(budget.currency)}}</span></template>
                <template v-else>{{ node.data.get_subtotal_manpower|currency(budget.currency) }}</template>
              </div>
              <div class="col-sm text-right col-100">
                <template v-if="hasChildren(node)"><span class="node-parent">{{node.data.subtotal_material|currency(budget.currency)}}</span></template>
                <template v-else>{{ node.data.get_subtotal_material|currency(budget.currency) }}</template>
              </div>
              <div class="col-sm text-right col-100">
                <template v-if="hasChildren(node)"><span class="node-parent">{{node.data.subtotal_subcontract|currency(budget.currency)}}</span></template>
                <template v-else>{{ node.data.get_subtotal_subcontract|currency(budget.currency) }}</template>
              </div>
              <div class="col-sm text-right col-100">
                <template v-if="hasChildren(node)"><span class="node-parent">{{node.data.subtotal_equipment|currency(budget.currency)}}</span></template>
                <template v-else>{{ node.data.get_subtotal_equipment|currency(budget.currency) }}</template>
              </div>
              <div class="col-sm text-right col-100">
                <template v-if="hasChildren(node)"><span class="node-parent">{{node.data.subtotal|currency(budget.currency)}}</span></template>
                <template v-else>{{node.data.get_subtotal|currency(budget.currency)}}</template>
                <!-- <span :class="{'node-parent': hasChildren(node)}">{{ getPartida(node)?node.data.get_subtotal:0|currency(budget.currency) }}</span> -->
              </div>

              <div>
                <b-dropdown variant="link" size="lg" no-caret>
                  <template slot="button-content">
                    &#x2630;<span class="sr-only">Opciones</span>
                  </template>
                  <b-dropdown-item @click="nuevo(node)" href="#">Adicionar</b-dropdown-item>
                  <b-dropdown-item v-if="!hasChildren(node)" @click="copiar(node)" href="#">Copiar</b-dropdown-item>
                  <b-dropdown-item v-if="!hasChildren(node)" @click="eliminar(node)" href="#">Eliminar...</b-dropdown-item>
                </b-dropdown>
              </div>
            </div>

          </div>

        </tree>
      </b-col>
    </b-row>
      </b-col>
  </b-row>
</template>

<script>
  import { mapGetters } from 'vuex'
  import LiquorTree from 'liquor-tree'
  import Loading from 'vue-loading-overlay'
  import 'vue-loading-overlay/dist/vue-loading.css'
  
  export default {
      components: {
          [LiquorTree.name]: LiquorTree,
          Loading
      },
      data() {
        return {
          isLoading: false,
          fullPage: true,
          selectedNode: null,
          treeFilter: "",
          tasks: [],
          tree: [],
          filter: null,
          node: "",
          title: "",
          treeOptions: {
            dnd: true,
          },
          data: null
        }
      },
      created() {
        this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
        this.isLoading = true
        this.$store.dispatch('budget/requestBudgetPartidas', this.$route.params.budget)
          .then(result => {
            this.isLoading = false;
          })
      },
      watch: {
        budget(){
          this.data = this.getTasks()
          this.$refs.tree.setModel(this.data)
        }
      },
      computed: {
        budget(){
          return this.$store.getters['budget/getSelectedBudget']
        },
        partidas(){
          return this.$store.getters['budget/getAvailableBudgetPartidas']
        }
      },
      mounted() {
        this.$refs.tree.$on("node:dragging:finish", ()=>{
          this.onSaveBudget({tree: this.$refs.tree.tree.model})
        })
      },
      methods: {
        refresh(){
          this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
          this.isLoading = true
          this.$store.dispatch('budget/requestBudgetPartidas', this.$route.params.budget)
            .then(result => {
              this.isLoading = false;
            })
          this.data = this.getTasks()
          this.$refs.tree.setModel(this.data)
        },
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
          const url = `/budget/api/tasks/${node.data.id}/`
          this.$swal({
            title: "¿Está seguro de eliminar la partida?",
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
            let total_manpower = 0
            let total_material = 0
            let total_subcontract = 0
            let total_equipment = 0
            node.children.forEach((item)=>{
              if(item.data.subtotal!==undefined){
              total += parseFloat(item.data.get_subtotal)
              total_manpower += parseFloat(item.data.get_subtotal_manpower)
              total_material += parseFloat(item.data.get_subtotal_material)
              total_subcontract += parseFloat(item.data.get_subtotal_subcontract)
              total_equipment += parseFloat(item.data.get_subtotal_equipment)
              }
            })
            this.$set(node.data, "subtotal", total)
            this.$set(node.data, "subtotal_manpower", total_manpower)
            this.$set(node.data, "subtotal_material", total_material)
            this.$set(node.data, "subtotal_subcontract", total_subcontract)
            this.$set(node.data, "subtotal_equipment", total_equipment)
          }
          return hasChildren
        },
        onSaveBudget(data) {
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
        getTasks(){
          if(this.budget){
            return this.budget.tree
          }else{
            return null
          }
        },
        getPartida(node){

          let partida = this.$store.getters['budget/getFilteredBudgetPartida'](node.data.id)[0]
          // Guardamos el subtotal de la partida para usarlo en el calculo de los subtotales por ramas
          this.$set(node.data, "get_subtotal", partida ? partida.get_subtotal : 0)
          this.$set(node.data, "get_subtotal_manpower", partida ? partida.get_subtotal_manpower * partida.quantity : 0)
          this.$set(node.data, "get_subtotal_material", partida ? partida.get_subtotal_material * partida.quantity : 0)
          this.$set(node.data, "get_subtotal_subcontract", partida ? partida.get_subtotal_subcontract * partida.quantity : 0)
          this.$set(node.data, "get_subtotal_equipment", partida ? (partida.get_subtotal_equipment + partida.get_subtotal_minor_tools) * partida.quantity : 0)
          return partida ? partida : null
        },
      }
  }
</script>
