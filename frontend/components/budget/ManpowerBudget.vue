<template>
  <b-row>
    <b-col md="12">
      <app-title :title="budget.code + ' - ' + budget.title"
        subTitle="Mano de Obra">
        <template slot="options">
            <b-button size="sm" @click="addItem">Adicionar Mano de Obra</b-button>
        </template>
      </app-title>

      <b-row class="bd-content">
        <b-col md="12" class="my-1">
          <b-row>
            <b-col md="9" class="my-1">
              <b-form-group class="mb-0">
                <b-input-group>
                  <b-form-input v-model="filter" placeholder="Escriba para buscar" />
                  <b-input-group-append>
                    <b-btn :disabled="!filter" @click="filter = ''">X</b-btn>
                  </b-input-group-append>
                </b-input-group>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="12">
              <b-table
                striped hover
                :items="items"
                :fields="fields"
                :filter="filter"
                >
                <template slot="get_tipo_epp_display" slot-scope="row">
                  <b-link @click="onShowDetail(row.item)" variant="link">{{row.item.get_tipo_epp_display}}</b-link>
                </template>
                <template slot="sueldo_bruto" slot-scope="row">
                  {{row.item.sueldo_bruto|currency(row.item.currency)}}
                </template>
                <template slot="get_costo_mes_contab" slot-scope="row">
                  {{row.item.get_costo_mes_contab|currency(row.item.currency)}}
                </template>
                <template slot="get_costo_mes_inmac" slot-scope="row">
                  {{row.item.get_costo_mes_inmac|currency(row.item.currency)}}
                </template>
                <template slot="get_costo_mes_con_relevo" slot-scope="row">
                  {{row.item.get_costo_mes_con_relevo|currency(row.item.currency)}}
                </template>
                <template slot="get_costo_mes_final" slot-scope="row">
                  {{row.item.get_costo_mes_final|currency(row.item.currency)}}
                </template>
                <template slot="get_cost_unit" slot-scope="row">
                  {{row.item.get_cost_unit|currency(budget.currency)}}
                </template>
                <template slot="actions" slot-scope="row">
                    <template>
                      <b-link @click="onEditItem(row.item)">
                          <icon name="pencil"></icon>
                      </b-link>
                      <span style="padding-right: 10px;"></span>
                      <b-link @click="onRemoveItem(row.item)">
                          <icon name="trash"></icon>
                      </b-link>
                    </template>
                </template>
              </b-table>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-col>
    <!-- ---------- -->
    <!-- Modal Form -->
    <b-modal 
      id="modalForm"
      ref="modalForm"
      :title="`${mode=='add' ? 'Adicionar': 'Actualizar'}`"
      @ok="onSubmit"
      @cancel="cancelModal"
      centered>
      <b-container fluid>
        <b-form-group id='manpower_group'
              :label="'Cargo'"
              label-for="manpower">
              <v-select id="manpower"
                        @input="onChangeValue"
                        :options="manpowers"
                        label="name"
                        placeholder="Escribe para buscar..."
                        :filterable="false"
                        @search="onManpowersSearch"
                        v-if="mode=='add'">
                <!-- <template slot="no-options">
                  Escriba para buscar...
                </template> -->
                <template slot="option" slot-scope="option">
                  <div>
                    {{ `${option.code} - ${option.name}` }}
                  </div>
                </template>
              </v-select>
              <div v-else>{{model.get_manpower_display}}</div>
        </b-form-group>
        <vue-form-generator 
            ref="vfg"
            :schema="schema" 
            :model="model"
            :options="formOptions">
        </vue-form-generator>
      </b-container>
    </b-modal>
    <!-- FIN: Modal Form  -->
  </b-row>
</template>

<script>

import { mapGetters } from 'vuex'
import Menu from "./nav/Menu.vue"
import Title from "../utils/Title.vue"
import '../../utils/icons/042-add'
// import Multiselect from 'vue-multiselect'

export default {
    components: {
        'app-menu': Menu,
        'app-title': Title,
    },
    data() {
        return {
          manpowers: [],
          // popoverShow: false,
          // selectedEPPBudget: null,
          searchQuery: '',
          // title: "Presupuesto de EPP",
          // items: [],
          payload: {},
          backData: {},
          model: {
            id: null,
            manpower: null,
            tipo_epp: null,
            sueldo_bruto: null,
            relevo_trabajo: null,
            relevo_descanso: null,
            get_manpower_display: null,
            currency: null,
            type_cost: null,
            has_medicina: true,
          },
          // titleGrid: "",
          mode: "",
          fields: [
              {key:'get_manpower_display', label: 'Puesto', sortable: true},
              {key:'get_tipo_epp_display', label: 'Tipo', sortable: true},
              {key:'sueldo_bruto', label: 'Sueldo bruto', sortable: true},
              {key:'get_costo_mes_contab', label: 'Costo mes cont.', sortable: true}, 
              {key:'get_costo_mes_inmac', label: 'Costo mes INMAC', sortable: true},
              {key:'get_costo_mes_con_relevo', label: 'Costo mes c/relevo', sortable: false},
              {key:'get_costo_mes_final', label: 'Costo mes', sortable: true},
              {key:'get_cost_unit', label: 'Costo unitario', sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: "",
          id: "",
          schema: {
            fields: [
              {
                type: 'select',
                label: 'Tipo de EPP',
                model: 'tipo_epp',
                required: true,
                values(){
                    var grupo = this.$store.getters['grupo/getFilteredGrupo']('TTR')
                    // console.log("grupo:", grupo)
                    return grupo.map((e)=>{return {id: e.id, name: e.nombre}})
                },
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Días de trabajo',
                model: 'relevo_trabajo',
                required: true,
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Días de descanso',
                model: 'relevo_descanso',
                required: true,
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Sueldo bruto',
                model: 'sueldo_bruto',
                required: true,
              },
              {
                type: 'select',
                label: 'Moneda',
                model: 'currency',
                required: true,
                values(){
                  return [
                    {id:"S", name: "Soles"},
                    {id:"D", name: "Dólares"}
                  ]
                }
              },
              {
                type: 'select',
                label: 'Tipo de costo',
                model: 'type_cost',
                required: true,
                values(){
                  return [
                    {id:"I", name: "Indirecto"},
                    {id:"D", name: "Directo"}
                  ]
                }
              },
              {
                type: "switch",
                label: "¿Tiene medicina?",
                model: "has_medicina",
                textOn: "Sí tiene",
                textOff: "No tiene"
              },
              {
                type: "switch",
                label: "¿Tiene gasto 1?",
                model: "has_gasto_1",
                textOn: "Sí tiene",
                textOff: "No tiene"
              },
              {
                type: "switch",
                label: "¿Tiene catering?",
                model: "has_catering",
                textOn: "Sí tiene",
                textOff: "No tiene"
              },
            ]
          },
          formOptions: {
            validateAfterLoad: false,
            validateAfterChanged: false,
            // validateAsync: true
          }
        }
    },
    created(){
      this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
      this.$store.dispatch('manpowerBudget/requestBudgetManpowers', {id: this.$route.params.budget})
      this.$store.dispatch('grupo/requestAvailableListGrupo', this.$route.params.budget)
      this.$store.dispatch('manpower/requestManpowers')
    },
    computed: {
      ...mapGetters({
          budget: 'budget/getSelectedBudget',
      }),
      items(){
        return this.$store.getters['manpowerBudget/getAvailableBudgetManpowers']
      },
    },
    methods: {
          onShowDetail(item){
            // this.titleGrid = item.get_tipo_epp_display
            this.$refs.modalGrid.show()
          },
          onClose() {
            this.$refs.modalForm.hide()
          },
          onCancel(){
            this.budget.meses_obra = this.backData.meses_obra
            this.onClose()
          },
          onEnable(){
            this.backData={
              meses_obra: this.budget.meses_obra
            }
            this.$refs.popover.$emit('enable')
          },
          addItem(){
            this.$set(this.model, "budget", this.budget.id )
            this.$set(this.model, "currency", 'S' )
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          onChangeValue(e) {
            if (Boolean(e)){
              this.model.sueldo_bruto = e.sueldo_bruto
              this.model.manpower = e.id
              this.model.currency = e.currency
              this.model.type_cost = e.type_cost
              // console.log("valor E", e)
              // this.model.tipo_epp = e.tipo_epp
              // this.model.budget = e.budget
              // this.model.relevo_trabajo = e.relevo_trabajo
              // this.model.relevo_descanso = e.relevo_descanso
              // this.model.business_cost = e.business_cost
              // this.model.type_material = e.class_cost
              // this.model.hours_equipment_operation = e.hours_equipment_operation
            }
          },
          onManpowersSearch (search, loading) {
            loading(true)
            this.$store.dispatch(`manpower/searchManpowers`, search).then(response => {
                this.manpowers = response
                loading(false)
            })
          },
          onSubmit(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfg.validate()
            // this.$set(this.model, "manpower", this.selectedManpower.id)
            if(isValid){
              this.$store.dispatch(`manpowerBudget/${this.mode}BudgetManpower`, this.model).then(response => {
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
                  showConfirmButton: false,
                  timer: 1500
                })
                // this.$store.dispatch('budget/requestBudgetManpowers', this.budget)
                this.$refs.modalForm.hide()
              }, error =>{
                  var msgError = ""
                  Object.keys(error.body).forEach((element) => {
                    msgError += `${element} : ${error.body[element]}\n`
                  });
                  this.$swal({
                    type: 'error',
                    title: 'Oops...',
                    text: 'Error, no se pudo guardar\n' + msgError
                  })
              })
            }
          },
          cancelModal(){
            this.$refs.modalForm.hide()
          },
          onEditItem(item){
            this.mode = "update"
            Object.keys(item).forEach(elemento=>this.$set(this.model, elemento, item[elemento] ))
            // console.log("editar: ", this.model)
            this.$refs.modalForm.show()
          },
          onRemoveItem(payload){
            this.$swal({
              title: `¿Está seguro de eliminar el ${payload.get_manpower_display}?`,
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sí, eliminar!'
            })
            .then((willDelete) => {
              if (willDelete.value) {
                this.$store.dispatch('manpowerBudget/deleteBudgetManpower', payload)
                  .then(response=>{
                    this.$swal({
                      position: 'top-end',
                      toast: true,
                      type: 'success',
                      title: 'Se eliminó correctamente.',
                      showConfirmButton: false,
                      timer: 1500
                    })
                    // this.$store.dispatch('requestEPPs', {epp: payload.epp})
                  }, err => {
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
          }
    }
  }
</script>