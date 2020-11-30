<template>
  <b-row>
    <b-col md="12">
      <app-title :title="budget.code + ' - ' + budget.title"
        subTitle="EPP">
        <template slot="options">
            <b-button size="sm" @click="addItem">Adicionar Presupuesto de EPP</b-button>
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
            <!-- <b-col md="3">
              <b-form-group horizontal id="class_meses_epp"
                label="Meses EPP: "><b-button @click="onEnable" id="popover-button-meses-epp" variant="link">{{budget.meses_epp}}</b-button>
              </b-form-group>
              <b-popover 
                target="popover-button-meses-epp"

                :show.sync="popoverShow"
                placement="auto"
                ref="popover"
                >
                <template slot="title">
                  <b-button @click="onClose" class="close" aria-label="Close">
                    <span class="d-inline-block" aria-hidden="true">&times;</span>
                  </b-button>
                  Interactive Content
                </template>
                <div>
                  <b-form-group
                    label="Meses"
                    label-for="popover-input-1"
                    label-cols="3"
                    class="mb-1"
                    description="Ingrese el número de meses del proyecto"
                    invalid-feedback="Este campo es obligatorio"
                  >
                    <b-form-input
                      ref="input1"
                      id="popover-input-1"
                      v-model="budget.meses_epp"
                      size="sm"
                    ></b-form-input>
                  </b-form-group>

                  <b-button @click="onCancel" size="sm" variant="danger">Cancel</b-button>
                  <b-button @click="onOk" size="sm" variant="primary">Ok</b-button>
                </div>
              </b-popover>
            </b-col> -->
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
                <template slot="get_costo" slot-scope="row">
                  {{row.item.get_costo|currency("S")}}
                </template>
                <template slot="get_costo_mes" slot-scope="row">
                  {{row.item.get_costo_mes|currency("S")}}
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
    <!-- Modal Grid -->
    <b-modal 
      id="modalGrid"
      size="xl"
      ref="modalGrid"
      :title="titleGrid"
      @ok="cancelModalGrid"
      centered>
      <b-container fluid>
        <b-col md="12">
          <app-title
          title="Presupuesto de EPP"
          subTitle="Detalle">
            <template slot="options">
                <b-button size="sm" @click="addItemGrid">Adicionar EPP</b-button>
            </template>
          </app-title>

          <b-row class="bd-content">
            <b-col md="12" class="my-1">
              <b-table
                striped hover
                :items="itemsGrid"
                :fields="fieldsGrid"
                >
                <template slot="get_parcial" slot-scope="row">
                  {{row.item.get_parcial|currency(budget.currency)}}
                </template>
                <template slot="actionsGrid" slot-scope="row">
                    <template>
                      <a @click="onEditItemGrid(row.item)">
                          <icon name="pencil"></icon>
                      </a>
                      <span style="padding-right: 10px;"></span>
                      <a @click="onRemoveItemGrid(row.item)">
                          <icon name="trash"></icon>
                      </a>
                    </template>
                </template>
              </b-table>
            </b-col>
          </b-row>
        </b-col>
        <!-- ----------- -->
        <!-- Modal Form Grid-->
        <b-modal 
          id="modalFormGrid"
          ref="modalFormGrid"
          :title="`${mode=='add' ? 'Adicionar': 'Actualizar'}`"
          @ok="onSubmitFormGrid"
          @cancel="cancelModalFormGrid"
          centered>
          <b-container fluid>
            <vue-form-generator 
                ref="vfgg"
                :schema="schemaGrid" 
                :model="modelGrid"
                :options="formOptions">
            </vue-form-generator>
          </b-container>
        </b-modal>
        <!-- FIN: Modal Form Grid -->
      </b-container>
    </b-modal>
    <!-- FIN: Modal Grid  -->
    
    <!-- Modal Form -->
    <b-modal 
      id="modalForm"
      ref="modalForm"
      :title="`${mode=='add' ? 'Adicionar': 'Actualizar'}`"
      @ok="onSubmit"
      @cancel="cancelModal"
      centered>
      <b-container fluid>
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

export default {
    components: {
        'app-menu': Menu,
        'app-title': Title,
    },
    data() {
        return {
          currentEPP: null,
          // popoverShow: false,
          selectedEPPBudget: null,
          searchQuery: '',
          title: "Presupuesto de EPP",
          // items: [],
          payload: {},
          backData: {},
          model: {
            tipo_epp: null,
          },
          titleGrid: "",
          mode: "",
          fieldsGrid: [
              {key:'get_material_display', label: 'Nombre de EPP', sortable: true},
              {key:'unidad', label: 'Unidad', sortable: true},
              {key:'periodo_reposicion', label: 'PR', sortable: true},
              {key:'get_demanda', label: 'Demanda', sortable: true},
              {key:'quantity', label: 'Cantidad', sortable: true},
              {key:'get_parcial', label: 'Parcial', formatter: value => value.toFixed(2), sortable: true},
              {key:'actionsGrid', label: 'Acciones'}
          ],
          fields: [
              {key:'get_tipo_epp_display', label: 'Tipo de EPP', sortable: true},
              {key:'get_costo', label: 'Costo Total', formatter: value => value.toFixed(2), sortable: true},
              {key:'get_costo_mes', label: 'Costo Mes', formatter: value => value.toFixed(2), sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: "",
          id: "",
          modelGrid: {
            material: null,
            unidad: "Und",
            periodo_reposicion: null,
            quantity: null,
          },
          schemaGrid: {
            fields: [
              {
                type: 'select',
                label: 'Material',
                model: 'material',
                required: true,
                values(){
                    var recurso = this.$store.getters['materialBudget/getAvailableBudgetMaterials']
                    console.log("recurso:", recurso)
                    return recurso.map((e)=>{return {id: e.id, name: e.get_resource_name}})
                },
              },
              {
                type: 'input',
                inputType: 'text',
                label: 'Unidad',
                model: 'unidad',
                required: true,
                validator: ['string']
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Periodo de Reposición',
                model: 'periodo_reposicion',
                required: true,
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Cantidad',
                model: 'quantity',
                required: true,
              },
            ]
          },
          schema: {
            fields: [
              {
                type: 'select',
                label: 'Tipo de EPP',
                model: 'tipo_epp',
                required: true,
                values(){
                    var grupo = this.$store.getters['grupo/getFilteredGrupo']("TTR")
                    console.log("grupo:", grupo)
                    return grupo.map((e)=>{return {id: e.id, name: e.nombre}})
                },
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
    // watch:{
    //     $route (to, from){
    //       this.$store.dispatch('grupo/requestAvailableListGrupo', {grupo: 'TTR'})
    //     }
    // },
    created(){
      this.$store.dispatch('grupo/requestAvailableListGrupo')
      let payload = {
        id: this.$route.params.budget,
        filter: {type_material: 'E'}
      }
      this.$store.dispatch('materialBudget/requestBudgetMaterials', payload)
      this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
      this.$store.dispatch('eppBudget/requestEPPs', this.$route.params.budget)
    },
    // mounted(){
    //   this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
    //   this.$store.dispatch('requestEPPs', this.$route.params.budget)
    //   this.$store.dispatch('requestEPPDetails')
    // },
    computed: {
      ...mapGetters({
          budget: 'budget/getSelectedBudget',
      }),
      items(){
        console.log("budgetid",this.$route.params.budget)
        return this.$store.getters['eppBudget/getEPPs']
      },
      itemsGrid(){

        return this.$store.getters['getEPPDetails']
        // return this.$store.getters['getFilteredEPPDetail'](this.currentEPP)
      },
    },
    methods: {
          // onGoToCost(vacuna){
          //   this.$store.dispatch('vacuna/requestBudgetInformation', budget)
          //   this.$router.push({name: 'budget-costing', params: {budget}})
          // },
          onShowDetail(item){
            this.currentEPP = item.id
            this.titleGrid = item.get_tipo_epp_display
            let payload = {
              epp_budget: this.currentEPP,
            }
            this.$store.dispatch('requestEPPDetails', payload)
            console.log("EPPs", payload)
            this.$refs.modalGrid.show()
          },
          onClose() {
            // this.popoverShow = false
            this.$refs.modalForm.hide()
          },
          // onCancel(){
          //   this.budget.meses_epp = this.backData.meses_epp
          //   this.onClose()
          // },
          // onHidden() {
          //   // Called just after the popover has finished hiding
          //   // Bring focus back to the button
          //   this.focusRef(this.$refs.button)
          // },
          // onEnable(){
          //   this.backData={
          //     meses_epp: this.budget.meses_epp
          //   }
          //   this.$refs.popover.$emit('enable')
          // },
          addItem(){
            this.$set(this.model, "budget", this.budget.id )
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          addItemGrid(){
            this.$set(this.modelGrid, "epp_budget", this.currentEPP )
            this.mode = "add"
            this.$refs.modalFormGrid.show()
          },
          onSubmit(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfg.validate()
            if(isValid){
              this.$store.dispatch(`eppBudget/${this.mode}EPP`, this.model).then(response => {
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
                  showConfirmButton: false,
                  timer: 1500
                })
                this.onClose()
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
          onSubmitFormGrid(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfgg.validate()
            if(isValid){
              this.$store.dispatch(`${this.mode}EPPDetail`, this.modelGrid).then(response => {
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
                  showConfirmButton: false,
                  timer: 1500
                })
                this.$nextTick(() => {
                  this.$refs.modalFormGrid.hide()  
                  this.$store.dispatch('eppBudget/requestEPPs', this.$route.params.budget)
                  // this.$store.dispatch('requestEPPDetails')
                })
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
          // onOk(){
          //   this.$set(this.payload, "id", this.budget.id)
          //   this.$set(this.payload, "meses_epp", this.budget.meses_epp)
          //   if(this.budget.meses_epp){
          //     this.$store.dispatch(`budget/updateBudget`, this.payload).then(response => {
          //       this.$swal({
          //         position: 'top-end',
          //         toast: true,
          //         type: 'success',
          //         title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
          //         showConfirmButton: false,
          //         timer: 1500
          //       })
          //       this.$store.dispatch('eppBudget/requestEPPs', this.$route.params.budget)
          //       this.$store.dispatch('requestEPPDetails')
          //       this.onClose()
          //     }, error =>{
          //         var msgError = ""
          //         Object.keys(error.body).forEach((element) => {
          //           msgError += `${element} : ${error.body[element]}\n`
          //         });
          //         this.$swal({
          //           type: 'error',
          //           title: 'Oops...',
          //           text: 'Error, no se pudo guardar\n' + msgError
          //         })
          //     })
          //   }
          // },
          cancelModal(){
            this.$refs.modalForm.hide()
          },
          cancelModalGrid(){
            this.$refs.modalGrid.hide()
          },
          cancelModalFormGrid(){
            this.$refs.modalFormGrid.hide()
          },
          onEditItem(item){
            this.mode = "update"
            Object.keys(item).forEach(elemento=>this.$set(this.model, elemento, item[elemento] ))
            this.$refs.modalForm.show()
          },
          onEditItemGrid(item){
            this.mode = "update"
            Object.keys(item).forEach(elemento=>this.$set(this.modelGrid, elemento, item[elemento] ))
            this.$refs.modalFormGrid.show()
          },
          onRemoveItem(payLoad){
            this.$swal({
              title: `¿Está seguro de eliminar el ${payLoad.get_tipo_epp_display}?`,
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sí, eliminar!'
            })
            .then((willDelete) => {
              if (willDelete.value) {
                this.$store.dispatch('eppBudget/deleteEPP', payLoad)
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
          },
          onRemoveItemGrid(payLoad){
            this.$swal({
              title: `¿Está seguro de eliminar el ${payLoad.get_material_display}?`,
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sí, eliminar!'
            })
            .then((willDelete) => {
              if (willDelete.value) {
                this.$store.dispatch('deleteEPPDetail', payLoad)
                  .then(response=>{
                    this.$swal({
                      position: 'top-end',
                      toast: true,
                      type: 'success',
                      title: 'Se eliminó correctamente.',
                      showConfirmButton: false,
                      timer: 1500
                    })
                    // this.$store.dispatch('requestEPPDetails', {epp: payLoad.epp})      
                    this.$store.dispatch('eppBudget/requestEPPs', this.$route.params.budget)
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