<template>
  <b-row>
    <b-col md="12">
      <app-title
      title="Listado de Presupuestos">
      <template slot="options">
          <b-button size="sm" @click="addItem" >Adicionar Presupuesto</b-button>
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
            <b-pagination size="md" :total-rows="totalRows" v-model="currentPage" :per-page="100"></b-pagination>
            <b-table
              striped hover :items="items" :fields="fields"
              :filter="filter">
              <template slot="actions" slot-scope="row">
                <b-dropdown variant="link" size="lg" no-caret>
                  <template slot="button-content">
                    &#x2630;
                  </template>
                  <b-dropdown-item @click="onEditItem(row.item)" href="#">Editar</b-dropdown-item>
                  <b-dropdown-item href="#" disabled>Copiar</b-dropdown-item>
                  <b-dropdown-item @click="onRemoveItem(row.item)" href="#">Eliminar</b-dropdown-item>
                </b-dropdown>
                <!-- <a @click="onEditItem(row.item)">
                    <icon name="pencil"></icon>
                </a>
                <span style="padding-right: 10px;"></span>
                <a @click="onRemoveItem(row.item)">
                    <icon name="trash"></icon>
                </a> -->
              </template>
              <template slot="image" slot-scope="row"><img :src="row.item.get_image_miniature_50_0" alt=""></template>
              <template slot="title" slot-scope="row">
                <b-link @click="onGoToDetail(row.item.id)">{{row.item.title}}</b-link>
              </template>
            </b-table>
            <b-pagination size="md" :total-rows="totalRows" v-model="currentPage" :per-page="100"></b-pagination>
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

// import filter from 'lodash/filter'
// import HandleItem from "./budget/HandleBudget.vue"
// import { mapGetters } from 'vuex'
// import '../utils/icons/042-add'
// import buildTree from '../../utils/tree'
// const url_api = '/budget/api/budgets/'

export default {
    data() {
        return {
          selectedBudget: null,
          searchQuery: '',
          title: "Presupuesto",
          handleTitle: "",
          filtered_items: [],
          // items: [],
          model: {
            id: null,
            title: null,
            client: null,
            currency: null,
            exchange_rate: null,
            ubicacion: null
          },
          mode: "",
          fields: [
              {key:'title', label: 'Título', sortable: true},
              {key:'get_client', label: 'Cliente', sortable: true},
              {key:'code', label: 'Código', sortable: true},
              {key:'get_ubicacion_display', label: 'Locación', sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: "",
          id: "",
          clientSelected: "",
          totalRows: 0,
          currentPage: 1,
            schema: {
              fields: [
                {
                  type: 'input',
                  inputType: 'text',
                  label: 'Titulo',
                  model: 'title',
                  required: true,
                  validator: ['string']
                },
                {
                  type: 'select',
                  label: 'Cliente',
                  model: 'client',
                  required: false,
                  values(){
                      var clients = this.$store.getters['client/getAvailableClients']
                      // console.log("clients:", clients)
                      return clients.map((e)=>{return {id: e.id, name: e.name}})
                  },
                  validator: ['number']
                },
                {
                  type: 'select',
                  label: 'Moneda',
                  model: 'currency',
                  required: false,
                  values(){
                      return [
                        { id: "S", name: "Soles" },
                        { id: "D", name: "Dólares" }
                      ]
                    },
                  validator: ['string'],
                  onChanged(model, schema, event) {
                    console.log(model, schema, event);
                  }
                },
                {
                  type: 'input',
                  inputType: 'number',
                  label: 'Tipo cambio',
                  model: 'exchange_rate',
                  required: false,
                },
                {
                  type: 'select',
                  label: 'Ubicación',
                  model: 'ubicacion',
                  required: false,
                  values(){
                      var ubicaciones = this.$store.getters['grupo/getFilteredGrupo']('UBC')
                      // console.log("ubicaciones:", ubicaciones)
                      return ubicaciones.map((e)=>{return {id: e.id, name: e.nombre}})
                  },
                  validator: ['number']
                },

              ]
            },
            formOptions: {
              validateAfterLoad: false,
              validateAfterChanged: false,
            }
        }
    },
    created(){
      // this.getItems()
      this.$store.dispatch('budget/requestBudgets')
      this.$store.dispatch('client/requestClients')
      this.$store.dispatch('grupo/requestAvailableListGrupo')
    },
    computed: {
      // ...mapGetters({
      //     budgets: 'getAvailableBudgets',
      // }),
      items(){
        return this.$store.getters['budget/getAvailableBudgets']
      },
      // shouldShowForm() {
      //     return this.selectedBudget !== null;
      // },
      // filteredBudgets() {
      //   return filter(this.budgets.results, (item) => {
      //       const hasBudgetMatch = (item.title.toLowerCase().indexOf(this.searchQuery) !== -1);
      //       // const hasManufacturerMatch = (item._embedded.manufacturer.name.toLowerCase().indexOf(this.searchQuery) !== -1);
      //       return hasBudgetMatch  // || hasManufacturerMatch;
      //   });
      // },
    },
    methods: {
          onGoToDetail(budget){
            this.$store.dispatch('budget/requestBudgetInformation', budget)
            this.$router.push({name: 'budget-partidas', params: {budget}})
          },
          addItem(){
            this.model = {}
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          onSubmit(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfg.validate()
            if(isValid){
              this.$store.dispatch(`budget/${this.mode}Budget`, this.model).then(response => {
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
                  console.log("Error>>>", error)
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
            // Object.keys(item).forEach(elemento=>this.$set(this.model, elemento, item[elemento] ))
            Object.keys(this.model).forEach(elemento=>this.$set(this.model, elemento, item[elemento] ))
            this.$refs.modalForm.show()
          },
          onRemoveItem(payLoad){
            this.$swal({
              title: `¿Está seguro de eliminar el ${payLoad.title}?`,
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sí, eliminar!'
            })
            .then((willDelete) => {
              if (willDelete.value) {
                // payLoad.is_deleted = true
                this.$store.dispatch('budget/removeBudget', payLoad)
                  .then(response=>{
                    this.$swal({
                      position: 'top-end',
                      toast: true,
                      type: 'success',
                      title: 'Se eliminó correctamente.',
                      showConfirmButton: false,
                      timer: 1500
                    })
                    // this.$store.dispatch('requestAvailableListGrupo', {grupo: payLoad.grupo})
                  }, err => {
                    var msgError = ""
                    console.log("Error>>>", err)
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
