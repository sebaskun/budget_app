<template>
  <b-row>
    <b-col md="12">
        <app-title
        title="Listado de Régimen"
        :subTitle="subtitle">
        <template slot="options">
            <b-button v-if="selectedRegimen" size="sm" @click="addItem">Adicionar Régimen</b-button>
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
              <b-form-group horizontal id="class_material_group"
                label="Régimen:"
                label-for="clase_material">
                <b-form-select
                  id="id_grupo"
                  v-model="selectedRegimen">
                  <option v-for="(item, indice) in regimenes" :value="item.id" :key="indice">{{item.nombre}}</option>
                </b-form-select>
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
              <template slot="sueldo" slot-scope="row">
                {{row.item.sueldo|currency(row.item.currency)}}
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
    import Title from "../utils/Title.vue"

    // import {RotateSquare2} from 'vue-loading-spinner'


    var numeral = require('numeral')
    export default {
        components: {
        'app-title': Title,
        },
        data() {
          return {
            subtitle: "",
            grupo: "",
            filter: "",
            selectedRegimen: "",
            newModel: true,
            model: {
              categoria_trabajador: null,
              currency: "S",
              sueldo: null
            },
            mode: "",
            fields: [
              {key:'get_categoria_trabajador_nombre', label:'Categoría'},
              {key:'sueldo', label:'Sueldo'},
              // {key:'get_tipo_nombre', label:'Tipo'},
              {key:'actions', label: 'Acciones'}
            ],
            schema: {
              fields: [
                  {
                    type: 'select',
                    label: 'Categoría',
                    model: 'categoria_trabajador',
                    values(){
                      let arr = this.$store.getters['grupo/getFilteredGrupo']('CTR')
                      return arr.map((e)=>{return {id: e.id, name: e.nombre}})
                      },
                    required: true,
                    validator: ['number']
                  },
              ],
              groups: [
                {
                  legend: "Sueldo",
                  fields: [
                    {
                      type: 'select',
                      label: 'Moneda',
                      model: 'currency',
                      values(){
                          return [
                            { id: "S", name: "Soles" },
                            // { id: "D", name: "Dólares" },
                          ]
                        },
                      required: true,
                      validator: ['string']
                    },
                    {
                      type: 'input',
                      inputType: 'number',
                      label: 'Sueldo',
                      model: 'sueldo',
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
        computed:{
          items(){
              // console.log("selectedRegimen:", this.selectedRegimen)
              let data = this.$store.getters['regimen/getFilteredListCategorias'](this.selectedRegimen)
              // console.log("data::___", data)
              return data
          },
          regimenes(){
            return this.$store.getters['grupo/getFilteredGrupo']('REG')
          }
        },
        watch:{
          $route (to, from){
            this.$store.dispatch('grupo/requestAvailableListGrupo')
            this.$store.dispatch('regimen/requestAvailableListRegimen')
          },
          selectedRegimen (to, from){

            this.subtitle = this.$store.getters['grupo/getSelectedGrupo'](to)[0].nombre
          }
        },
        created() {
          this.$store.dispatch('grupo/requestAvailableListGrupo')
          this.$store.dispatch('regimen/requestAvailableListRegimen')
        },
        methods: {

          addItem(){
            this.model = {currency: "S"}
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          getSelectedRegimen(){
              return this.selectedRegimen
          },
          onSubmit(evt){
            // console.log("onSubmin:", evt)
            evt.preventDefault()
            this.$set(this.model, "regimen", this.selectedRegimen)
            var isValid = this.$refs.vfg.validate()
            // console.log('Es valido:', isValid)
            if(isValid){
              this.$store.dispatch(`regimen/${this.mode}Regimen`, this.model).then(response => {
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
                  showConfirmButton: false,
                  timer: 1500
                })
                this.$store.dispatch('regimen/requestAvailableListRegimen')
                // this.$store.dispatch('requestAvailableListRegimen', {regimen: this.selectedRegimen})
                this.$refs.modalForm.hide()
              }, error =>{
                  // console.log("error", error)
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
                this.$store.dispatch('updateGrupo', payLoad)
                  .then(response=>{
                    this.$swal({
                      position: 'top-end',
                      toast: true,
                      type: 'success',
                      title: 'Se eliminó correctamente.',
                      showConfirmButton: false,
                      timer: 1500
                    })
                    this.$store.dispatch('grupo/requestAvailableListGrupo', {grupo: payLoad.grupo})
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
