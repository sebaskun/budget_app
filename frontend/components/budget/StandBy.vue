<template>
  <b-row>
    <b-col md="12">
      <app-title :title="budget.code + ' - ' + budget.title" subTitle="Stand By">
      </app-title>
      <b-row class="bd-content">
        <b-col md=12 class="my-1">
          <section class="view-data">
            <table class="table table-striped">
              <col width="18%">
              <col width="10%">
              <col width="10%">
              <col width="10%">
              <col width="10%">
              <col width="10%">
              <col width="10%">
              <col width="10%">
              <col width="10%">
              <col width="50px">
              <thead>
                <tr>
                  <th colspan="10">
                    <span class="price float-right">
                      EQUIPOS: {{equipments.total|currency(budget.currency)}}
                    </span>
                  </th>
                </tr>
                <tr>
                  <th class="text-center" style="vertical-align:middle">Descripción</th>
                  <th class="text-center" style="vertical-align:middle">Cantidad</th>
                  <th class="text-center" style="vertical-align:middle">Tiempo Valorizar</th>
                  <th class="text-center" style="vertical-align:middle">Horas por día</th>
                  <th class="text-center" style="vertical-align:middle">Horas estimadas</th>
                  <th class="text-center" style="vertical-align:middle">Horas APU</th>
                  <th class="text-center" style="vertical-align:middle">Stand By</th>
                  <th class="text-center" style="vertical-align:middle">Costo Hora</th>
                  <th class="text-center" style="vertical-align:middle">Costo Stand By</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr is="equipment-stand-by"
                  v-for="(equipment, index) in equipments.items"
                  :equipment="equipment"
                  :budget="budget"
                  :key="index"
                  @updated="updatedEquipment">
                </tr>
              </tbody>
            </table>
          </section>
          <section class="view-data">
            <table class="table table-striped">
              <col width="17%">
              <col width="9%">
              <col width="9%">
              <col width="9%">
              <col width="9%">
              <col width="9%">
              <col width="9%">
              <col width="9%">
              <col width="9%">
              <col width="9%">
              <col width="50px">
              <thead>
                <tr>
                  <th colspan="10">
                    <span class="price float-right">
                      MANO DE OBRA: {{manpowers.total|currency(budget.currency)}}
                    </span>
                  </th>
                </tr>
                <tr>
                  <th class="text-center" style="vertical-align:middle">Descripción</th>
                  <th class="text-center" style="vertical-align:middle">Cantidad</th>
                  <th class="text-center" style="vertical-align:middle">Tiempo Valorizar</th>
                  <th class="text-center" style="vertical-align:middle">Horas estimadas</th>
                  <th class="text-center" style="vertical-align:middle">Horas APU</th>
                  <th class="text-center" style="vertical-align:middle">Stand By</th>
                  <th class="text-center" style="vertical-align:middle">Costo Hora</th>
                  <th class="text-center" style="vertical-align:middle">Costo Stand By</th>
                  <th class="text-center" style="vertical-align:middle">Rehidratación (Caja de agua)</th>
                  <th class="text-center" style="vertical-align:middle">EPP</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr is="manpower-stand-by"
                  v-for="(manpower, index) in manpowers.items"
                  :manpower="manpower"
                  :budget="budget"
                  :key="index"
                  @updated="updatedManpower">
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td style="font-weight:bold">{{manpowers.total|currency(budget.currency)}}</td>
                  <td style="font-weight:bold">{{manpowers.hydration|currency(budget.currency)}}</td>
                  <td style="font-weight:bold">{{manpowers.epp|currency(budget.currency)}}</td>
                </tr>
              </tfoot>
            </table>
          </section>
        </b-col>
      </b-row>
    </b-col>
  </b-row>
</template>

<script>
  // import ImportTask from "./task/ImportTask.vue"

  import ManpowerStandBy from "./standby/ManpowerStandByItem.vue"
  import EquipmentStandBy from "./standby/EquipmentStandByItem.vue"
  import Menu from "./nav/Menu.vue"
  import Title from "../utils/Title.vue"
  // import jQuery from 'jquery'
  // import {RotateSquare2} from 'vue-loading-spinner'

  const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }

  const url_api = `/budget/api/budgets/`
  var numeral = require('numeral')
  export default {
      components: {
        // 'app-resource-budget': ResourceBudget,
        'manpower-stand-by': ManpowerStandBy,
        'equipment-stand-by': EquipmentStandBy,
        'app-menu': Menu,
        'app-title': Title
          // RotateSquare2
      },
      data() {
        return {
          // refreshApu: false,
          manpowers: {},
          equipments: {},
          showAPU: false,
          errors: [],
          tasks: [],
          lenTasks: 0,
          budget: "",
          show: true,
          str_action: "Crear",
          id: "",
          showImportForm: false,
          showManpowerForm: false,
          filter: null,
          max: 100,
          progress: 0,
          count: 0,
          node: "",
          title: "",
          typeResource: "",
          editing: false,
          budgetId: null,
          taskId: "",
          task: "",
        }
      },
      created() {
        this.budgetId = this.$route.params.budget
        if(this.$route.query.task){
          this.taskId = this.$route.query.task
          this.getTask()
        }
        this.getBudget()
      },

      methods: {
        updatedManpower(){
          this.getManpowerBudget()
        },
        updatedEquipment(){
          this.getEquipmentBudget()
        },
        getTask() {
          let url = `/budget/api/tasks/${this.taskId}/`
          this.$http.get(url)
            .then((response) => {
              this.task = response.data
            })
            .catch((err) => {
              console.log('error en getTasks: ', err)
            })
        },
        getBudget(){
          let url = `${url_api}${this.budgetId}/`
          this.$http.get(url)
            .then((response) => {
                this.budget = response.data
                this.getManpowerBudget()
                this.getEquipmentBudget()
            })
            .catch((err) => {
              console.log("error en getBudget", err)
            })
        },
        getManpowerBudget(){
          let url = `/budget/api/budgets/${this.budget.id}/manpower/standby`
          this.$http.get(url)
            .then((response) => {
              this.manpowers = response.data
            })
            .catch((err) => {
              console.log("error en getManpowerBudget::", err)
            })
        },
        getEquipmentBudget(){
          let url = `/budget/api/budgets/${this.budget.id}/equipment/standby`
          this.$http.get(url)
            .then((response) => {
              this.equipments = response.data
            })
            .catch((err) => {
              console.log("error en getEquipmentBudget::", err)
            })
        },
        onShow(resourceBudget){
          let resources={
            manpower: {title: "Mano de obra"},
            material: {title: "Material"},
            equipment: {title: "Equipo"}
          }
          this.typeResource = resourceBudget
          this.title = resources[resourceBudget].title
        },
      }
  }
</script>
