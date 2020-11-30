<template>
  <b-row>
    <b-col md="12">
      <app-title :title="budget.code + ' - ' + budget.title"
        subTitle="Gastos Generales">
        <!-- <template slot="options">
          <b-button size="sm">boton 1</b-button>
        </template> -->
      </app-title>

      <b-row class="bd-content">
        <b-col md="12" class="my-1">
          <section class="view-data">
            <table class="table table-striped">
              <thead>
                <th colspan="10">
                    <span class="price float-right">Checklist Directos Fijos que dependen del Plazo de Obra {{totalOverhead|currency(budget.currency)}} | 100.00%</span>
                </th>
              </thead>
            </table>
          </section>
          <!-- INICIO: PERSONAL DE DIRECCION TECNICA EN OBRA -->

          <section class="view-data">
            <table class="table table-striped">
              <col width="33%">
              <col width="13%">
              <col width="13%">
              <col width="13%">
              <col width="13%">
              <col width="13%">
              <col width="50px">
              <thead>
                <tr>
                  <th colspan="10">
                    <span class="price float-right">
                      PERSONAL DE DIRECCION TECNICA EN OBRA: {{manpowers.total|currency(budget.currency)}} | {{getRatio(manpowers.total)|decimal('0.00%')}}
                    </span>
                  </th>
                </tr>
                <tr>
                  <th class="text-center" style="vertical-align:middle">Descripción</th>
                  <th class="text-center" style="vertical-align:middle">Cantidad</th>
                  <th class="text-center" style="vertical-align:middle">Mes</th>
                  <th class="text-center" style="vertical-align:middle">Costo empresa</th>
                  <th class="text-center" style="vertical-align:middle">Total</th>
                  <th class="text-center" style="vertical-align:middle">% s/R</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr is="manpower-overhead"
                  v-for="(manpower, index) in manpowers.items"
                  :manpower="manpower"
                  :budget="budget"
                  :key="index"
                  :totalOverhead=totalOverhead
                  @updated="updatedManpower">
                </tr>
              </tbody>
            </table>
          </section>
          <!-- FIN: PERSONAL DE DIRECCION TECNICA EN OBRA -->

          <section class="view-data">
            <table class="table table-striped">
              <col width="33%">
              <col width="13%">
              <col width="13%">
              <col width="13%">
              <col width="13%">
              <col width="13%">
              <col width="50px">
              <thead>
                <tr>
                  <th colspan="10">
                    <span class="price float-right">COSTOS DE STAND BY: {{totalStandby|currency(budget.currency)}} | {{getRatio(totalStandby)|decimal('0.00%')}}</span>
                  </th>
                </tr>
                <tr>
                  <th class="text-center" style="vertical-align:middle">Descripción</th>
                  <th class="text-center" style="vertical-align:middle">Cantidad</th>
                  <th class="text-center" style="vertical-align:middle">Mes</th>
                  <th class="text-center" style="vertical-align:middle">Costo empresa</th>
                  <th class="text-center" style="vertical-align:middle">Total</th>
                  <th class="text-center" style="vertical-align:middle">% s/R</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>STAND BY PERSONAL (Glb)</td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td class="text-right">{{standby.manpower|currency}}</td>
                  <td class="text-right">{{getRatio(standby.manpower)|decimal('0.00%')}}</td>
                  <td></td>
                </tr>
                <tr>
                  <td>STAND BY EQUIPOS (Glb)</td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td class="text-right">{{standby.equipment|currency}}</td>
                  <td class="text-right">{{getRatio(standby.equipment)|decimal('0.00%')}}</td>
                  <td></td>
                </tr>
              </tbody>
            </table>
          </section>

          <section class="view-data">
            <table class="table table-striped">
              <col width="32%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="50px">
              <thead>
                <tr>
                  <th colspan="10">
                    <span class="price float-right">TALLER MECÁNICO: {{workshops.total|currency(budget.currency)}} | {{getRatio(workshops.total)|decimal('0.00%')}}</span>
                  </th>
                </tr>
                <tr>
                  <th class="text-center" style="vertical-align:middle">Descripción</th>
                  <th class="text-center" style="vertical-align:middle">Cantidad</th>
                  <th class="text-center" style="vertical-align:middle">Mes</th>
                  <th class="text-center" style="vertical-align:middle">% Amortización</th>
                  <th class="text-center" style="vertical-align:middle">Costo empresa</th>
                  <th class="text-center" style="vertical-align:middle">Total</th>
                  <th class="text-center" style="vertical-align:middle">% s/R</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr is="material-overhead"
                  v-for="(workshop, index) in workshops.items"
                  :item="workshop"
                  :budget="budget"
                  :key="index"
                  :total-overhead=totalOverhead
                  @updated="updatedMaterial">
                </tr>
              </tbody>
            </table>
          </section>

          <section class="view-data">
            <table class="table table-striped">
              <col width="32%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="50px">
              <thead>
                <tr>
                  <th colspan="10">
                    <span class="price float-right">TÓPICO SALUD: {{medicals.total|currency(budget.currency)}} | {{getRatio(medicals.total)|decimal('0.00%')}}</span>
                  </th>
                </tr>
                <tr>
                  <th class="text-center" style="vertical-align:middle">Descripción</th>
                  <th class="text-center" style="vertical-align:middle">Cantidad</th>
                  <th class="text-center" style="vertical-align:middle">Mes</th>
                  <th class="text-center" style="vertical-align:middle">% Amortización</th>
                  <th class="text-center" style="vertical-align:middle">Costo empresa</th>
                  <th class="text-center" style="vertical-align:middle">Total</th>
                  <th class="text-center" style="vertical-align:middle">% s/R</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr is="material-overhead"
                  v-for="(medical, index) in medicals.items"
                  :item="medical"
                  :budget="budget"
                  :key="index"
                  :total-overhead=totalOverhead
                  @updated="updatedMaterial">
                </tr>
              </tbody>
            </table>
          </section>

          <section class="view-data">
            <table class="table table-striped">
              <col width="32%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="50px">
              <thead>
                <tr>
                  <th colspan="10">
                    <span class="price float-right">GASTO OPERATIVO, OFICINA, CONTINGENCIA: {{operatives.total|currency(budget.currency)}} | {{getRatio(operatives.total)|decimal('0.00%')}}</span>
                  </th>
                </tr>
                <tr>
                  <th class="text-center" style="vertical-align:middle">Descripción</th>
                  <th class="text-center" style="vertical-align:middle">Cantidad</th>
                  <th class="text-center" style="vertical-align:middle">Mes</th>
                  <th class="text-center" style="vertical-align:middle">% Amortización</th>
                  <th class="text-center" style="vertical-align:middle">Costo empresa</th>
                  <th class="text-center" style="vertical-align:middle">Total</th>
                  <th class="text-center" style="vertical-align:middle">% s/R</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr is="material-overhead"
                  v-for="(operative, index) in operatives.items"
                  :item="operative"
                  :budget="budget"
                  :key="index"
                  :total-overhead=totalOverhead
                  @updated="updatedMaterial">
                </tr>
              </tbody>
            </table>
          </section>

          <section class="view-data">
            <table class="table table-striped">
              <col width="32%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="11%">
              <col width="50px">
              <thead>
                <tr>
                  <th colspan="10">
                    <span class="price float-right">VARIOS: {{various.total|currency(budget.currency)}} | {{getRatio(various.total)|decimal('0.00%')}}</span>
                  </th>
                </tr>
                <tr>
                  <th class="text-center" style="vertical-align:middle">Descripción</th>
                  <th class="text-center" style="vertical-align:middle">Cantidad</th>
                  <th class="text-center" style="vertical-align:middle">Mes</th>
                  <th class="text-center" style="vertical-align:middle">% Amortización</th>
                  <th class="text-center" style="vertical-align:middle">Costo empresa</th>
                  <th class="text-center" style="vertical-align:middle">Total</th>
                  <th class="text-center" style="vertical-align:middle">% s/R</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr is="material-overhead"
                  v-for="(one, index) in various.items"
                  :item="one"
                  :budget="budget"
                  :key="index"
                  :total-overhead=totalOverhead
                  @updated="updatedMaterial">
                </tr>
              </tbody>
            </table>
          </section>
        </b-col>
      </b-row>
    </b-col>
  </b-row>
</template>

<script>

  import ManpowerOverhead from "./overhead/ManpowerOverheadItem.vue"
  import MaterialOverhead from "./overhead/MaterialOverheadItem.vue"
  import { mapState } from 'vuex'
  import Menu from "./nav/Menu.vue"
  import Title from "../utils/Title.vue"

  const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }

  const url_api = `/budget/api/budgets/`
  var numeral = require('numeral')
  export default {
      components: {
        'manpower-overhead': ManpowerOverhead,
        'material-overhead': MaterialOverhead,
        'app-menu': Menu,
        'app-title': Title
      },
      data() {
        return {
          budget: "",
          budgetId: null,
          errors: [],
          id: "",
          manpowers: {},
          medicals: [],
          operatives: [],
          show: true,
          standby: {},
          task: "",
          taskId: "",
          title: "",
          typeResource: "",
          various: [],
          workshops: [],
        }
      },
      computed:{
        totalOverhead(){
          let total = this.manpowers.total + this.totalStandby +
            this.workshops.total + this.operatives.total + this.medicals.total + this.various.total
          return total
        },
        totalStandby(){
          return this.standby.manpower + this.standby.equipment
        },
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
        updatedMaterial(){
          this.getMaterials('W')
          this.getMaterials('M')
          this.getMaterials('O')
          this.getMaterials('V')
        },
        updatedManpower(){
          this.getManpowerBudget()
        },
        getRatio(value){
          return value / this.totalOverhead
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
                this.getStandby()
                this.getMaterials('W')
                this.getMaterials('M')
                this.getMaterials('O')
                this.getMaterials('V')
                // this.getEquipmentBudget()
            })
            .catch((err) => {
              console.log("error en getBudget", err)
            })
        },
        getStandby(){
          let url = `/budget/api/budgets/${this.budgetId}/standby/overhead`
          this.$http.get(url)
            .then((response) => {
              this.standby = response.data
            })
            .catch((err) => {
              console.log("error en getStandBy::", err)
            })
        },
        getManpowerBudget(){
          let url = `/budget/api/budgets/${this.budgetId}/manpower/overhead`
          this.$http.get(url)
            .then((response) => {
              this.manpowers = response.data
            })
            .catch((err) => {
              console.log("error en getManpowerBudget::", err)
            })
        },
        getMaterials(typeMaterial){
          let url = `/budget/api/budgets/${this.budgetId}/material/${typeMaterial}/overhead`
          this.$http.get(url)
            .then((response) => {
              if(typeMaterial=="W"){
                this.workshops = response.data
              }
              if(typeMaterial=="M"){
                this.medicals = response.data
              }
              if(typeMaterial=="O"){
                this.operatives = response.data
              }
              if(typeMaterial=="V"){
                this.various = response.data
              }
            })
            .catch((err) => {
              console.log("error en getMaterialBudget::", err)
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
      },
      // mounted() {
      //   this.$nextTick(function () {
      //     console.log("Total overhead:::::", this.totalOverhead)
      //   })
      // }
  }

</script>
