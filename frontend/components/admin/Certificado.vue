<template>
  <b-row>
    <b-col md="12">
        <app-title
        title="Listado de Certificados">
        <template slot="options">
            <b-button size="sm" @click="addItem">Adicionar Certificado</b-button>
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
            <b-table
              striped hover
              :items="items"
              :fields="fields"
              :filter="filter">
              <template slot="importe" slot-scope="row">
                {{row.item.importe|currency(row.item.currency)}}
              </template>
              <template slot="actions" slot-scope="row">
                <a @click="onEditItem(row.item)">
                    <icon name="pencil"></icon>
                </a>
                <span style="padding-right: 10px;"></span>
                <a @click="onRemoveItem(row.item)">
                    <icon name="trash"></icon>
                </a>
              </template>
            </b-table>
          </section>
        </b-col>
      </b-row>
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

    import { mapState } from 'vuex'
    // import Title from "../utils/Title.vue"

    // import {RotateSquare2} from 'vue-loading-spinner'


    var numeral = require('numeral')
    export default {
        // components: {
        // 'app-title': Title,
        // },
        data() {
          return {
            grupo: "",
            filter: "",
            selectedRegimen: "",
            newModel: true,
            model: {
              categoria_trabajador: null,
              currency: 'S',
              sueldo: null
            },
            mode: "",
            fields: [
              {key:'nombre', label:'Nombre'},
              {key:'importe', label:'Importe'},
              {key:'actions', label: 'Acciones'}
            ],
            schema: {
              fields: [
                {
                  type: 'input',
                  inputType: 'text',
                  label: 'Nombre',
                  model: 'nombre',
                  required: true,
                  validator: ['string']
                },
              ],
              groups: [
                {
                  legend: "Importe",
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
                      label: 'Importe',
                      model: 'importe',
                      required: true
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
        computed:{
          items(){
              return this.$store.getters['getAvailableListCertificado']
          },
        },
        created() {
          this.$store.dispatch('requestAvailableListCertificado')
        },
        methods: {
          addItem(){
            this.model = {currency: "S"}
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          onSubmit(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfg.validate()
            if(isValid){
              this.$store.dispatch(`${this.mode}Certificado`, this.model).then(response => {
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
                  showConfirmButton: false,
                  timer: 1500
                })
                this.$store.dispatch('requestAvailableListCertificado', {regimen: this.selectedRegimen})
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
              title: `¿Está seguro de eliminar el ${payLoad.nombre}?`,
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sí, eliminar!'
            })
            .then((willDelete) => {
              if (willDelete.value) {
                payLoad.activo = false
                this.$store.dispatch('updateCertificado', payLoad)
                  .then(response=>{
                    this.$swal({
                      position: 'top-end',
                      toast: true,
                      type: 'success',
                      title: 'Se eliminó correctamente.',
                      showConfirmButton: false,
                      timer: 1500
                    })
                    this.$store.dispatch('requestAvailableListGrupo', {grupo: payLoad.grupo})
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
      },
    }
</script>
