<template>
  <b-row>
    <b-col md="12">
        <app-title
        :title="`Listado de ${grupo}`">
        <template slot="options">
            <b-button v-if="grupo" size="sm" @click="addGrupo">{{`Adicionar ${grupo}`}}</b-button>
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
              <b-form-group id="class_material_group"
                label-cols-sm="4"
                label-cols-lg="3"
                label="Grupo:"
                label-for="clase_material">
                <b-form-select
                  id="id_grupo"
                  v-model="selectedGrupo">
                  <option v-for="(item, indice) in grupos" :value="item.id" :key="indice">{{item.nombre}}</option>
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
      id="modalGrupo"
      ref="modalGrupo"
      :noCloseOnBackdrop="true"
      :title="`Adicionar ${grupo}`"
      @ok="onSubmit"
      @cancel="cancelModal"
      centered>
      <b-container fluid>
        <vue-form-generator 
            :schema="schema" 
            :model="model"
            :isNewModel="newModel"
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
            grupo: "",
            filter: "",
            selectedGrupo: "",
            newModel: true,
            model: {},
            mode: "",
            fields: [
              {key:'nombre', label:'Nombre'},
              {key:'get_grupo_nombre', label:'Grupo'},
              {key:'actions', label: 'Acciones'}
            ],
            grupos: [
                {id: "CTR", nombre: "CATEGORIA TRABAJADOR"},
                {id: "TTR", nombre: "TIPO DE EPP"},
                {id: "UBC", nombre: "UBICACIÓN"},
                {id: "MON", nombre: "MONEDA"},
                {id: "REG", nombre: "REGIMEN"},
            ],
            schema: {
              fields: [
                  {
                  type: 'input',
                  inputType: 'text',
                  label: 'Nombre',
                  model: 'nombre',
                  placeholder: 'Your name',
                  featured: true,
                  required: true
                  }
              ]
            },
            formOptions: {
              validateAfterLoad: true,
              validateAfterChanged: true,
              validateAsync: true
            }
          }
        },
        // watch:{
        //   selectedGrupo(newValue, oldValue){


        //   }
        // },
        computed:{
          items(){
            const selected = this.grupos.filter(item=>item.id===this.selectedGrupo)
            if(selected.length>0){
              this.grupo = selected[0].nombre
            }else{
              this.grupo = ""
            }
            return this.$store.getters['grupo/getFilteredGrupo'](this.selectedGrupo)
          }
        },
        created() {
          this.$store.dispatch('grupo/requestAvailableListGrupo')
        },
        methods: {
          // onSelectedGrupo(){
          //   const selected = this.grupos.filter(item=>item.id===this.selectedGrupo)
          //   if(selected.length>0){
          //       this.grupo = selected[0].nombre
          //       this.$store.dispatch('grupo/requestAvailableListGrupo', {grupo: this.selectedGrupo})
          //   }else{
          //       this.grupo = ""
          //   }
          // },
          addGrupo(){
            this.model = {}
            this.mode = "add"
            this.$refs.modalGrupo.show()
          },
          getSelectedGrupo(){
              return this.selectedGrupo
          },
          onSubmit(){
            this.$set(this.model, "grupo", this.selectedGrupo)
            this.$store.dispatch(`grupo/${this.mode}Grupo`, this.model).then(response => {
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
                  showConfirmButton: false,
                  timer: 1500
                })
                this.$refs.modalGrupo.hide()
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
              
          },
          cancelModal(){
            this.$refs.modalGrupo.hide()
          },
          onEditItem(item){
            console.log("Item:", item)
            this.mode = "update"
            Object.keys(item).forEach(elemento=>this.$set(this.model, elemento, item[elemento] ))
            // this.model = {
            //   pk: item.pk,
            //   nombre: item.nombre,
            // }
            this.$refs.modalGrupo.show()
            // this.$store.dispatch('updateGrupo', payLoad).then(response => {
            //   console.log()
            // })
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
                this.$store.dispatch('grupo/updateGrupo', payLoad)
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
