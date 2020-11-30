<template>
  <b-row>
    <b-col md="12">
      <app-title
      title="Listado de Subcontratos">
      <template slot="options">
          <b-button size="sm" @click="addItem" >Adicionar Subcontrato</b-button>
      </template>
      </app-title>
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
      <b-row class="bd-content">

        <b-col md="12" class="my-1">
          <section class="view-data">
            <b-pagination size="md" :total-rows="totalRows" v-model="currentPage" :per-page="100"></b-pagination>
            <b-table
              striped hover :items="items" :fields="fields"
              :filter="filter">
              <template slot="cost" slot-scope="row">
                  {{row.item.cost|currency(row.item.currency)}}
              </template>
              <template slot="actions" slot-scope="row">
                <b-link @click="onEditItem(row.item)">
                    <icon name="pencil"></icon>
                </b-link>
                <span style="padding-right: 10px;"></span>
                <b-link @click="onRemoveItem(row.item)">
                    <icon name="trash"></icon>
                </b-link>
              </template>
            </b-table>
            <b-pagination size="md" :total-rows="totalRows" v-model="currentPage" :per-page="100"></b-pagination>
          </section>
        </b-col>
      </b-row>
    </b-col>
    
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
    <!-- ---------- -->
  </b-row>
</template>

<script>

import { mapGetters } from 'vuex'
import '../utils/icons/042-add'

export default {
    data() {
        return {
          // currentVacuna: null,
          totalRows:0,
          currentPage:1,
          selectedSubcontract: null,
          searchQuery: '',
          title: "Subcontract",
          // items: [],
          model: {
            code: "",
            name: "",
            unit: "Und",
            currency: "D",
            cost:"",
            // costo_unitario_transporte:"",
            // ratio_perdida:"",
            description:"",
          },
          mode: "",
          fields: [
              {key:'code', label: 'Código', sortable: true},
              {key:'name', label: 'Nombre', sortable: true},
              {key:'unit', label: 'Unidad', sortable: true},
              {key:'cost', label: 'Costo en Origen', sortable: true},
              // {key:'costo_unitario_transporte', label: 'Costo Unit Transporte', sortable: true},
              // {key:'ratio_perdida', label: '% de Pérdida', sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: "",
          id: "",
          schema: {
            fields: [
              {
                type: 'input',
                inputType: 'text',
                label: 'Código',
                model: 'code',
                required: true,
                validator: ['string']
              },
              {
                type: 'input',
                inputType: 'text',
                label: 'Nombre',
                model: 'name',
                required: true,
                validator: ['string']
              },
              {
                type: 'input',
                inputType: 'text',
                label: 'Unidad',
                model: 'unit',
                required: false,
                validator: ['string']
              },
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
                model: 'cost',
                required: true,
              },
              // {
              //   type: 'input',
              //   inputType: 'number',
              //   label: 'Costo Unit Transp',
              //   model: 'costo_unitario_transporte',
              //   required: true,
              // },
              // {
              //   type: 'input',
              //   inputType: 'number',
              //   label: '% de Pérdida',
              //   model: 'ratio_perdida',
              //   required: true,
              // },
              {
                type: 'textArea',
                // inputType: 'textarea',
                label: 'Descripción',
                model: 'description',
                hint: "Max 500 characters",
                max: 500,
                placeholder: "¿Cómo es el Subcontrato?",
                rows: 4,
                validator: ['string']
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
      // this.$store.dispatch('categoryEquipment/requestCategoryEquipments')
      this.$store.dispatch('subcontract/requestSubcontracts').then(response => {
        this.totalRows = response.totalRows
      })
    },
    computed: {
      // ...mapGetters({
      //     budgets: 'getAvailableBudgets',
      // }),
      items(){
        return this.$store.getters['subcontract/getSubcontracts']
      },
    },
    watch: {
      currentPage(to, from){
        let payLoad = {
          page: to,
          search: this.filter,
        }
        this.$store.dispatch('subcontract/requestSubcontracts', payLoad).then(response => {
          this.totalRows = response.totalRows
        })
      },
      filter: function (to, from) {
            if (this.currentPage != 1){
                this.currentPage = 1
            } 
            else {
              let payLoad = {
                page: this.currentPage,
                search: this.filter,
              }
              this.$store.dispatch('subcontract/requestSubcontracts', payLoad).then(response => {
                this.totalRows = response.totalRows
              })
            }
        }
    },
    methods: {
          // onGoToCost(vacuna){
          //   this.$store.dispatch('vacuna/requestBudgetInformation', budget)
          //   this.$router.push({name: 'budget-costing', params: {budget}})
          // },
          addItem(){
            // this.model = {moneda: "S"}
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          onSubmit(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfg.validate()
            if(isValid){
              this.$store.dispatch(`subcontract/${this.mode}Subcontract`, this.model).then(response => {
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
                  showConfirmButton: false,
                  timer: 1500
                })
                // this.$store.dispatch('budget/requestBudgets')
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
            this.$refs.modalForm.show()
          },
          onRemoveItem(payLoad){
            this.$swal({
              title: `¿Está seguro de eliminar el ${payLoad.name}?`,
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sí, eliminar!'
            })
            .then((willDelete) => {
              if (willDelete.value) {
                // payLoad.is_deleted = true
                this.$store.dispatch('subcontract/removeSubcontract', payLoad)
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
                    console.log("Error>>>", err)
                    Object.keys(error.body).forEach((element) => {
                      msgError += `${element} : ${error.body[element]}\n`
                    });
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