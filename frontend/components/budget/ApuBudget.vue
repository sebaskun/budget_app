<template>
  <b-row>
    <app-title 
      :title="budget.code + ' - ' + budget.title">
      <template v-if="task" slot="subTitle"><app-handle-task :task="task"/></template>
    </app-title>
    <b-col md="12" class="my-1">
      <b-row class="bd-content">
        <b-col md="8" class="my-1">
          <b-form-group label="Rendimiento:">
            <label v-if="task">{{task.efficiency|decimal("0.00")}}</label>
          </b-form-group>
        </b-col>
        <b-col md="4">
          <b-card v-if="task" bg-variant="light" header="Sub total" class="text-center" :title="totalTask|currency(budget.currency)"/>
        </b-col>


        <br>
        <template v-if="task">
          <app-resource-task :task="task" :budget="budget" ref="material" type-resource="material" title="Material" v-model="totalMaterial"></app-resource-task>
          <app-resource-task :task="task" :budget="budget" ref="subcontract" type-resource="subcontract" title="Subcontrato" v-model="totalSubcontract"></app-resource-task>
          <app-resource-task :task="task" :budget="budget" ref="equipment" type-resource="equipment" title="Equipo" v-model="totalEquipment" :subtotal-manpower="totalManpower"></app-resource-task>
          <app-resource-task :task="task" :budget="budget" ref="manpower" type-resource="manpower" title="Mano de obra" v-model="totalManpower"></app-resource-task>
        </template>

      </b-row>
    </b-col>

  </b-row>

</template>

<script>
  // import Tree from "./task/Tree.vue"
  import ResourceBudget from "./ResourceBudget.vue"
  // import jQuery from 'jquery'
  import HandleTask from './task/HandleTask.vue'
  import ResourceTask from './task/resource/Resource.vue'
  import Menu from "./nav/Menu.vue"
  import { mapGetters } from 'vuex'

  // const treeSearch = require('tree-search')
  var _ = require('lodash')

export default {
      components: {
          'app-handle-task': HandleTask,
          'app-resource-task': ResourceTask,
          'app-menu': Menu
      },
      data() {
        return {
          budgetId: null,
          taskId: null,
          filter: null,
          title: "",
          typeResource: "",
          efficiency: null,
          reCalcEfficiency: false,
          partida: {},
          totalMaterial: 0,
          totalManpower: 0,
          totalSubcontract: 0,
          totalEquipment: 0,
        }
      },
      created() {
        this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
        this.$store.dispatch('budget/requestBudgetPartidas', this.$route.params.budget)
      },
      watch:{
        '$route'(to, from){
          this.budgetId = this.$route.params.budget
          this.taskId = this.$route.params.task
        },
        efficiency(new_value, old_value){
          if (old_value != null){
            this.reCalcEfficiency = true
            this.$eventHub.$emit("reCalcEfficiency", new_value)
          }
        },
        // budgetId(value, oldValue){
        //   this.$store.dispatch('budget/requestBudgetInformation', value)
        // },
        // taskId(value, oldValue){
        //   this.$store.dispatch('requestTaskInformation', value)

        // },

      },
      computed: {
        ...mapGetters({
            budget: 'budget/getSelectedBudget',
        }),
        task() {
          let data = this.$store.getters['budget/getFilteredBudgetPartida'](this.$route.params.task)
          return data[0]
        },
        totalTask() {
          let total_ = this.totalManpower + this.totalMaterial + this.totalEquipment + this.totalSubcontract
          return total_

        }
      },
      methods: {

      }
}




</script>
