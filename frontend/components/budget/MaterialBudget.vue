<template>
  <b-row>
    <b-col md="12">
      <app-title :title="budget.code + ' - ' + budget.title"
        subTitle="Material">
        <template slot="options">
            <b-button size="sm" @click="addItem">Adicionar Material</b-button>
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
            <b-col md="3">
              <b-form-group horizontal id="class_material_group"
                label="Clase de material:"
                label-for="clase_material">
                <b-form-select
                  id="class_material"
                  v-model="selectedType"
                  @change="onSelectType"
                  :options="typeMaterials">
                </b-form-select>
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
                <template slot="price" slot-scope="row">
                  {{row.item.price|currency(row.item.currency)}}
                </template>
                <template slot="get_costo_obra" slot-scope="row">
                  {{row.item.get_costo_obra|currency(row.item.currency)}}
                </template>
                <template slot="get_costo_transporte" slot-scope="row">
                  {{row.item.get_costo_transporte|currency(row.item.currency)}}
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
        <b-form-group id='group'
              :label="'Recurso'">
              <v-select id="resource"
                        @input="onChangeValue"
                        :options="resources"
                        label="name"
                        placeholder="Escribe para buscar..."
                        :filterable="false"
                        @search="onResourcesSearch"
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
              <div v-else>{{model.get_resource_label}}</div>
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
          resources: [],
          // popoverShow: false,
          // selectedEPPBudget: null,
          searchQuery: '',
          // title: "Presupuesto de EPP",
          // items: [],
          payload: {},
          backData: {},
          // selectedResource: null,
          model: {
            id: null,
            price: null,
            budget: null,
            currency: null,
            ratio_perdida: "1.00",
            unit: null,
          },
          // titleGrid: "",
          mode: "",
          fields: [
              {key:'get_resource_label', label: 'Nombre', sortable: true},
              {key:'price', label: 'Costo Origen', sortable: true},
              // {key:'get_costo_transporte', label: 'Costo Transporte', sortable: false},     ----- Activar Posteriormente
              {key:'get_costo_obra', label: 'Costo en Obra', sortable: true}, 
              {key:'ratio_perdida', label: '% Pérdida', sortable: true},
              {key:'get_cost_unit', label: 'Costo unitario', sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: "",
          id: "",
          selectedType: "S",
          typeMaterials: [
            { value: "S", text: "Estándar"},
            { value: "M", text: "Médico"},
            { value: "W", text: "Taller"},
            { value: "O", text: "Operativo"},
            { value: "V", text: "Varios"},
            { value: "I", text: "Insumo médico"},
            { value: "E", text: "EPP"},
          ],
          // typeMaterials(){
          //   return getter
          // },
          schema: {
            fields: [
              {
                type: 'select',
                label: 'Moneda',
                model: 'currency',
                required: true,
                values(){
                    return [
                      { id: "S", name: "Soles" },
                      { id: "D", name: "Dólares" }
                    ]
                  },
                validator: ['string']
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Costo Origen',
                model: 'price',
                required: true,
              },
              {
                type: 'input',
                inputType: 'string',
                label: 'Unidad',
                model: 'unit',
                required: true,
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Costo Unit Transp',
                model: 'costo_unitario_transporte',
                disabled: true,
                required: false,
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Distancia (km)',
                model: 'distancia',
                disabled: true,
                required: false,
              },
              {
                type: 'input',
                inputType: 'number',
                label: '% de Pérdida',
                model: 'ratio_perdida',
                required: true,
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
      let payload = {
        id: this.$route.params.budget,
        filter: {type_material: this.selectedType}
      }
      this.$store.dispatch('materialBudget/requestBudgetMaterials', payload)
      // this.$store.dispatch('budget/requestBudgetManpowers', this.$route.params.budget)
      this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
      this.$store.dispatch('grupo/requestAvailableListGrupo', this.$route.params.budget)
      this.$store.dispatch('materialBudget/setTypeMaterial', this.selectedType)
      // this.$store.dispatch('manpower/requestManpowers')

      // this.$store.dispatch('requestEPPs')
    },
    mounted(){
      this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
    },
    computed: {
      ...mapGetters({
          budget: 'budget/getSelectedBudget',
      }),
      items(){
        let items = this.$store.getters['materialBudget/getAvailableBudgetMaterials']
        // console.log('Items>>>', items)
        return items
      },
    },
    methods: {
      onSelectType(){
        let payload = {
          id: this.$route.params.budget,
          filter: {type_material: this.selectedType}
        }
        this.$store.dispatch('materialBudget/setTypeMaterial', this.selectedType)
        // console.log("dispatch filtro>>>", payload)
        this.$store.dispatch('materialBudget/requestBudgetMaterials', payload)
      },
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
        this.$set(this.model, "budget", this.budget.id )
        // this.$set(this.model, "currency", 'S' )
        this.mode = "add"
        this.$refs.modalForm.show()
      },
      onChangeValue(e) {
        if (Boolean(e)){
          // console.log("Model::", this.model)
          // this.$set(this.model, "price", e.cost )
          this.model.material = e.id
          this.model.currency = e.currency
          this.model.price = e.cost
          this.model.unit = e.unit
          this.model.type_material = e.class_cost
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
      onResourcesSearch (search, loading) {
        loading(true)
        console.log ("search>>>", search)
        let payload = {
          search,
          class_cost: this.selectedType
        }
        this.$store.dispatch(`material/requestMaterials`, payload).then(response => {
            this.resources = response.data
            loading(false)
        })
      },
      onSubmit(evt){
        evt.preventDefault()
        var isValid = this.$refs.vfg.validate()
        // this.$set(this.model, "manpower", this.selectedManpower.id)
        if(isValid){
          this.$store.dispatch(`materialBudget/${this.mode}BudgetMaterial`, this.model).then(response => {
            this.$swal({
              position: 'top-end',
              toast: true,
              type: 'success',
              title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
              showConfirmButton: false,
              timer: 1500
            })
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
      onRemoveItem(payLoad){
        this.$swal({
          title: `¿Está seguro de eliminar el ${payLoad.get_resource_label}?`,
          type: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Sí, eliminar!'
        })
        .then((willDelete) => {
          if (willDelete.value) {
            this.$store.dispatch('materialBudget/deleteBudgetMaterial', payLoad)
              .then(response=>{
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: 'Se eliminó correctamente.',
                  showConfirmButton: false,
                  timer: 1500
                })
                
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