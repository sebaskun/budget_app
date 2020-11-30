<template>
  <b-row>
    <b-col md="12">
      <app-title
      title="Listado de Presupuesto de Vacunas">
      <template slot="options">
          <b-button size="sm" @click="addItem" >Adicionar Presupuesto de Vacunas</b-button>
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
              striped hover :items="items" :fields="fields"
              :filter="filter">
              <template slot="get_costo_vacuna" slot-scope="row">
                  {{row.item.get_costo_vacuna|currency(row.item.moneda)}}
              </template>
              <template slot="nombre" slot-scope="row">
                  <b-link @click="onShowDetail(row.item)" variant="link">{{row.item.nombre}}</b-link>
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
              <!-- <template slot="image" slot-scope="row"><img :src="row.item.get_image_miniature_50_0" alt=""></template>
              <template slot="title" slot-scope="row">
                <b-link @click="onGoToCost(row.item.id)">{{row.item.title}}</b-link>
              </template> -->
            </b-table>
          </section>
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
          title="Presupuesto de Vacuna"
          subTitle="Detalle">
            <template slot="options">
                <b-button size="sm" @click="addItemGrid">Adicionar Vacuna</b-button>
            </template>
          </app-title>

          <b-row class="bd-content">
            <b-col md="12" class="my-1">
              <b-table
                striped hover
                :items="itemsGrid"
                :fields="fieldsGrid"
                >
                <template slot="get_precio_parcial" slot-scope="row">
                  {{row.item.get_precio_parcial|currency(row.item.get_material_moneda)}}
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
  </b-row>
</template>

<script>

import { mapGetters } from 'vuex'
import '../utils/icons/042-add'

export default {
    data() {
        return {
          currentVacuna: null,
          selectedVacuna: null,
          searchQuery: '',
          title: "Vacuna",
          // items: [],
          model: {
            nombre: null,
            ubicacion: null,
            moneda: "S",
          },
          titleGrid: "",
          mode: "",
          fieldsGrid: [
              {key:'get_material_display', label: 'Vacuna', sortable: true},
              {key:'quantity', label: 'Cantidad', sortable: true},
              {key:'get_precio_parcial', label: 'Precio Parcial', formatter: value => value.toFixed(2), sortable: true},
              {key:'actionsGrid', label: 'Acciones'}
          ],
          fields: [
              {key:'nombre', label: 'Nombre', sortable: true},
              {key:'get_ubicacion_display', label: 'Ubicación', sortable: true},
              {key:'get_costo_vacuna', label: 'Importe Total', formatter: value => value.toFixed(2), sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: "",
          id: "",
          modelGrid: {
            material: null,
            quantity: null,
            observacion: '',
          },
          schemaGrid: {
            fields: [
              {
                type: 'select',
                label: 'Material',
                model: 'material',
                required: true,
                values(){
                    var recurso = this.$store.getters['material/getMaterials']
                    console.log("recurso::::::", recurso)
                    return recurso.map((e)=>{return {id: e.id, name: e.name}})
                },
              },
              {
                type: 'input',
                inputType: 'number',
                label: 'Cantidad',
                model: 'quantity',
                required: true,
              },
              {
                type: 'input',
                inputType: 'text',
                label: 'Observación',
                model: 'observacion',
                required: false,
                validator: ['string']
              },
            ]
          },
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
              {
                type: 'select',
                label: 'Ubicación',
                model: 'ubicacion',
                required: false,
                values(){
                    var grupo = this.$store.getters['grupo/getAvailableListGrupo']
                    console.log("grupo:", grupo)
                    return grupo.map((e)=>{return {id: e.id, name: e.nombre}})
                },
                // validator: ['number']
              },
              {
                type: 'select',
                label: 'Moneda',
                model: 'moneda',
                required: true,
                values(){
                    return [
                      { id: "S", name: "Soles" },
                      // { id: "D", name: "Dólares" }
                    ]
                  },
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
      this.$store.dispatch('grupo/requestAvailableListGrupo', {grupo: 'UBC'})
      this.$store.dispatch('material/requestMaterials', {class_cost: 'I'})
      this.$store.dispatch('vacuna/requestAvailableListVacunas')
      this.$store.dispatch('vacunaDetail/requestVacunaDetails')
    },
    computed: {
      // ...mapGetters({
      //     budgets: 'getAvailableBudgets',
      // }),
      items(){
        return this.$store.getters['vacuna/getVacunas']
      },
      itemsGrid(){
        // return this.$store.getters['vacunaDetail/getVacunaDetails']
        return this.$store.getters['vacunaDetail/getFilteredVacunaDetail'](this.currentVacuna)
      },
    },
    methods: {
          // onGoToCost(vacuna){
          //   this.$store.dispatch('vacuna/requestBudgetInformation', budget)
          //   this.$router.push({name: 'budget-costing', params: {budget}})
          // },
          onShowDetail(item){
            this.currentVacuna = item.id
            this.titleGrid = item.nombre
            this.$refs.modalGrid.show()
          },
          addItem(){
            this.model = {moneda: "S"}
            this.mode = "add"
            this.$refs.modalForm.show()
          },
          addItemGrid(){
            this.$set(this.modelGrid, "vacuna", this.currentVacuna )
            this.mode = "add"
            this.$refs.modalFormGrid.show()
          },
          onSubmit(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfg.validate()
            if(isValid){
              this.$store.dispatch(`vacuna/${this.mode}Vacuna`, this.model).then(response => {
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
          onSubmitFormGrid(evt){
            evt.preventDefault()
            var isValid = this.$refs.vfgg.validate()
            if(isValid){
              this.$store.dispatch(`vacunaDetail/${this.mode}VacunaDetail`, this.modelGrid).then(response => {
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
                  this.$store.dispatch('vacuna/requestAvailableListVacunas')
                  this.$store.dispatch('vacunaDetail/requestVacunaDetails')
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
              title: `¿Está seguro de eliminar el ${payLoad.nombre}?`,
              type: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sí, eliminar!'
            })
            .then((willDelete) => {
              if (willDelete.value) {
                payLoad.is_deleted = true
                this.$store.dispatch('vacuna/updateVacuna', payLoad)
                  .then(response=>{
                    this.$swal({
                      position: 'top-end',
                      toast: true,
                      type: 'success',
                      title: 'Se eliminó correctamente.',
                      showConfirmButton: false,
                      timer: 1500
                    })
                    this.$store.dispatch('vacuna/requestAvailableListVacunas', {vacuna: payLoad.vacuna})
                    this.$store.dispatch('vacunaDetail/requestVacunaDetails')
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
                payLoad.is_deleted = true
                payLoad.quantity = 0
                this.$store.dispatch('vacunaDetail/updateVacunaDetail', payLoad)
                  .then(response=>{
                    this.$swal({
                      position: 'top-end',
                      toast: true,
                      type: 'success',
                      title: 'Se eliminó correctamente.',
                      showConfirmButton: false,
                      timer: 1500
                    })
                    this.$store.dispatch('vacunaDetail/requestVacunaDetails', {epp: payLoad.epp})
                    this.$store.dispatch('vacuna/requestAvailableListVacunas')
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