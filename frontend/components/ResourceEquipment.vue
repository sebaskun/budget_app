<template>
  <b-row>
    <b-col md="12">
      <app-title
      title="Listado de Equipos"
      subTitle="Recursos">
      <template slot="options">
          <b-button size="sm" @click="addItem" >Adicionar Equipo</b-button>
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
          <b-col md="3">
            <b-form-group id="category_equipment">
              <!-- label="Categoría:"
              label-for="category_equipment"> -->
              <b-container class = "bv-example-row">
                <b-row>
                  <b-col md="3">Categoría</b-col>
                  <b-col md="9">
                    <b-form-select
                      id="category_equipment"
                      v-model="selectedType"
                      @change="onSelectType"
                      :options="types()">
                      <template slot="first">
                          <option :value="null">--- Todas ---</option>
                      </template>
                    </b-form-select>
                  </b-col>
                </b-row>
              </b-container>
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
          selectedEquipment: null,
          searchQuery: '',
          selectedType: null,
          title: "Equipo",
          // items: [],
          model: {
            code: "",
            name: "",
            unit: "Hr",
            currency: "D",
            cost:"",
            hours_equipment_operation:"",
            category:"",
            description:"",
          },
          mode: "",
          fields: [
              {key:'code', label: 'Código', sortable: true},
              {key:'name', label: 'Nombre', sortable: true},
              {key:'unit', label: 'Unidad', sortable: true},
              {key:'cost', label: 'Costo hs Cotizado', sortable: true},
              {key:'hours_equipment_operation', label: 'H.Operac.', sortable: true},
              {key:'get_category_display', label: 'Categoría', sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: "",
          id: "",
          types(){
            var categorias = this.$store.getters['categoryEquipment/getCategoryEquipments']
            console.log("categorias:", categorias)
            return categorias.map((e)=>{return {value: e.id, text: e.name}})
          },
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
                label: 'Costo hs Cotizado',
                model: 'cost',
                required: true,
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'H.Operac.',
                model: 'hours_equipment_operation',
                required: true,
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Potencia',
                model: 'potencia',
                required: true,
              },
              {
                type: "switch",
                label: "¿Tiene combutible?",
                model: "has_combustible",
                textOn: "Sí tiene",
                textOff: "No tiene"
              },
              {
                type: 'select',
                label: 'Tipo Combustible',
                model: 'tipo_combustible',
                required: false,
                values(){
                    return [
                      { id: "GO", name: "GasOil" },
                      { id: "GS", name: "Gasolina" }
                    ]
                  },
                validator: ['string']
              },
              {
                type: 'select',
                label: 'Categoría',
                model: 'category',
                required: false,
                values(){
                    var categorias = this.$store.getters['categoryEquipment/getCategoryEquipments']
                    console.log("categorias:", categorias)
                    return categorias.map((e)=>{return {id: e.id, name: e.name}})
                },
                // validator: ['number']
              },
              {
                type: 'textArea',
                // inputType: 'textarea',
                label: 'Descripción',
                model: 'description',
                hint: "Max 500 characters",
                max: 500,
                placeholder: "¿Cómo es el Equipo?",
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
      this.$store.dispatch('categoryEquipment/requestCategoryEquipments')
      this.$store.dispatch('equipment/requestEquipments').then(response => {
        this.totalRows = response.totalRows
      })
    },
    computed: {
      // ...mapGetters({
      //     budgets: 'getAvailableBudgets',
      // }),
      items(){
        return this.$store.getters['equipment/getEquipments']
      },
    },
    watch: {
      currentPage(to, from){
        let payLoad = {
          page: to,
          category: this.selectedType,
          search: this.filter,
        }
        this.$store.dispatch('equipment/requestEquipments', payLoad).then(response => {
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
                category: this.selectedType,
                search: this.filter,
              }
              this.$store.dispatch('equipment/requestEquipments', payLoad).then(response => {
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
          onSelectType(){
            console.log("Entré al filtro", this.selectedType)
            let filtro = {
              page: this.currentPage,
              category: this.selectedType,
              search: this.filter,
            }
            this.$store.dispatch('equipment/requestEquipments', filtro).then(response => {
              this.totalRows = response.totalRows
            })
          },
          addItem(){
            // this.model = {moneda: "S"}
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          onSubmit(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfg.validate()
            if(isValid){
              this.$store.dispatch(`equipment/${this.mode}Equipment`, this.model).then(response => {
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
                  console.log("Error:", error)
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
                this.$store.dispatch('equipment/removeEquipment', payLoad)
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