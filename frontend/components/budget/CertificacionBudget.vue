<template>
  <b-row>
      <app-title :title="budget.code + ' - ' + budget.title"
        subTitle="Certificación">
        <template slot="options">
            <b-button size="sm" @click="addItem">Adicionar Certificacion</b-button>
        </template>
      </app-title>


        <b-col md="12" class="my-1">
              <b-form-group class="mb-0">
                <b-input-group>
                  <b-form-input v-model="filter" placeholder="Escriba para buscar" />
                  <b-input-group-append>
                    <b-btn :disabled="!filter" @click="filter = ''">X</b-btn>
                  </b-input-group-append>
                </b-input-group>
              </b-form-group>

              <b-table
                striped hover
                :items="items"
                :fields="fields"
                :filter="filter"
                >
                <template slot="importe" slot-scope="row">
                {{row.item.importe|currency(row.item.moneda)}}
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
          selectedCertificacion: null,
          searchQuery: '',
          title: "Presupuesto de Certificación",
          // items: [],
          model: {
            certificado: null,
            moneda: null,
            importe: null,
          },
          mode: "",
          fields: [
              {key:'get_certificado_display', label: 'Nombre', sortable: true},
              {key:'importe', label: 'Importe', sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: "",
          id: "",
            schema: {
              fields: [
                {
                  type: 'select',
                  label: 'Nombre',
                  model: 'certificado',
                  required: true,
                  values(){
                    var certificados = this.$store.getters['getAvailableListCertificado']
                    console.log("certificados:", certificados)
                    return certificados.map((e)=>{return {id: e.id, name: e.nombre}})
                  },
                  onChanged(model, to, from) {
                    console.log("to", to, "from", from)
                    // if(this.mode=='add'){
                      let certificado = this.$store.getters["getFilteredCertificado"](to)
                      console.log("entre", certificado)
                      if (certificado[0]){
                            this.$set(this.model, "moneda", certificado[0].currency)
                            this.$set(this.model, "importe", certificado[0].importe)
                      }
                    // }
                  }
                },
              ],
              groups: [
                {
                  legend: "Importe",
                  fields: [
                    {
                      type: 'select',
                      label: 'Moneda',
                      model: 'moneda',
                      required: true,
                      values(){
                          return [
                            { id: "S", name: "Soles" },
                            { id: "D", name: "Dólares" }
                          ]
                        },
                      default: "S",
                      validator: ['string']
                    },
                    {
                      type: 'input',
                      inputType: 'number',
                      label: 'Importe',
                      model: 'importe',
                      required: true,
                    },
                  ]
                }
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
      this.$store.dispatch('requestAvailableListCertificado')
      let payload = {
        budget: this.$route.params.budget,
      }
      this.$store.dispatch('requestCertificaciones', payload)
    },
    computed: {
      ...mapGetters({
          budget: 'budget/getSelectedBudget',
      }),
      items(){
        return this.$store.getters['getCertificaciones']
      },
    },
    methods: {
          // onGoToCost(vacuna){
          //   this.$store.dispatch('vacuna/requestBudgetInformation', budget)
          //   this.$router.push({name: 'budget-costing', params: {budget}})
          // },
          addItem(){
            this.$set(this.model, "budget", this.budget.id )
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          onSubmit(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfg.validate()
            if(isValid){
              this.$store.dispatch(`${this.mode}Certificacion`, this.model).then(response => {
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
            this.$refs.modalForm.show()
          },
          onRemoveItem(payLoad){
            this.$swal({
              title: `¿Está seguro de eliminar el ${payLoad.get_certificado_display}?`,
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sí, eliminar!'
            })
            .then((willDelete) => {
              if (willDelete.value) {
                this.$store.dispatch('deleteCetificacion', payLoad)
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