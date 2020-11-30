<template>
  <b-row>
    <b-col md="12">
      <app-title :title="budget.code + ' - ' + budget.title"
        :subTitle="labelTypeResource">
        <template slot="options">
            <b-button size="sm" @click="showModal">{{`Adicionar ${labelTypeResource}`}}</b-button>
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
                label-for="clase_material"
                v-if="typeResource=='material'">
                <b-form-select
                  id="class_material"
                  v-model="classMaterial"
                  @input="onFilterClass"
                  :options="filtros">
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
                :filter="filter">
                <!-- @filtered="onFilterClass"> -->
                <!-- <template slot="actions" slot-scope="row">
                  <a @click.stop="onRemoveItem(row.item.id)"><icon name="trash"></icon></a>
                </template> -->
                <template slot="price" slot-scope="row">
                  {{row.value | currency(row.item.currency) }}
                </template>
                <template slot="get_cost_unit" slot-scope="row">
                  {{row.value | currency(budget.currency) }}
                </template>
                <template slot="epp_cost" slot-scope="row">
                  {{row.value | currency(row.item.currency) }}
                </template>
                <template slot="business_cost" slot-scope="row">
                  {{row.value | currency(row.item.currency) }}
                </template>
                <template slot="actions" slot-scope="row">
                    <template>
                      <a @click="onEditItem(row.item)">
                          <icon name="pencil"></icon>
                      </a>
                      <span style="padding-right: 10px;"></span>
                      <a @click="onRemoveItem(row.item)">
                          <icon name="trash"></icon>
                      </a>
                    </template>
                </template>
              </b-table>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-col>
    <b-modal 
      id="modalResource"
      ref="modalResource"
      :title="`Adicionar ${labelTypeResource}`"
      @ok="onSubmit"
      @cancel="cancelModal"
      centered>
      <b-container fluid>
          <b-form>
            <b-form-group id='resource_group'
              :label="labelTypeResource"
              label-for="resource">
              <v-select id="resource"
                        @input="onChangeValue"
                        v-model="selectedResource"
                        :options="resources"
                        label="name"
                        :filterable="false"
                        @search="onResourcesSearch">
                <template slot="no-options">
                  Escriba para buscar...
                </template>
                <template slot="option" slot-scope="option">
                  <div>
                    {{ `${option.code} - ${option.name}` }}
                  </div>
                </template>
              </v-select>
            </b-form-group>

            <b-row>
              <b-col lg="4">
                <b-form-group id="unit_group"
                  label="Unidad:"
                  label-for="unit">
                  <b-form-input
                    id="unit"
                    type="text"
                    v-model="form.unit"
                    placeholder="Unidad">
                  </b-form-input>
                </b-form-group>
              </b-col>
              <b-col lg="4">
                <b-form-group id="currency_group"
                  label="Moneda:"
                  label-for="currency">
                  <b-form-select
                    id="currency"
                    v-model="form.currency">
                    <option value="D">Dólares</option>
                    <option value="S">Soles</option>
                  </b-form-select>
                </b-form-group>
              </b-col>
              <b-col lg="4">
                <b-form-group id="cost_group"
                  v-if="typeResource!='manpower'"
                  label="Costo unitario:"
                  label-for="price">
                  <b-form-input
                    id="price"
                    type="number"
                    step=".1"
                    v-model="form.price"
                    placeholder="Precio">
                  </b-form-input>
                </b-form-group>
              </b-col>
            </b-row>
            <!-- <template v-if="typeResource=='manpower'">
              <b-row>
                <b-col lg="4">
                  <b-form-group id="epp_cost_group"
                    label="Costo EPP:"
                    label-for="epp_cost">
                    <b-form-input
                      id="epp_cost"
                      type="number"
                      step=".01"
                      v-model="form.epp_cost"
                      placeholder="Costo EPP">
                    </b-form-input>
                  </b-form-group>
                </b-col>
                <b-col lg="4">
                  <b-form-group id="business_cost_group"
                    label="Costo Empresarial:"
                    label-for="business_cost">
                    <b-form-input
                      id="business_cost"
                      type="number"
                      step=".01"
                      v-model="form.business_cost"
                      placeholder="Costo Empresarial">
                    </b-form-input>
                  </b-form-group>
                </b-col>
                <b-col lg="4">
                  <b-form-group id="type_cost_group"
                    label="Tipo de costo:"
                    label-for="type_cost">
                    <b-form-select
                      id="type_cost"
                      v-model="form.type_cost">
                      <option value="D">Directo</option>
                      <option value="I">Indirecto</option>
                    </b-form-select>
                  </b-form-group>
                </b-col>
              </b-row>
            </template> -->
            <template v-if="typeResource=='material'">
              <b-row>
                <b-col lg="4">
                  <b-form-group id="type_material_group"
                    label="Tipo de material:"
                    label-for="type_material">
                    <b-form-select
                      id="type_material"
                      v-model="form.type_material"
                      :options="filtros">
                    </b-form-select>
                  </b-form-group>
                </b-col>
              </b-row>
            </template>
            <template v-if="typeResource=='equipment'">
              <b-row>
                <b-col lg="4">
                  <b-form-group id="hours_equipment_operation_group"
                    label="Horas de operación por día:"
                    label-for="hours_equipment_operation">
                    <b-form-input
                      id="hours_equipment_operation"
                      type="number"
                      step="0.50"
                      v-model="form.hours_equipment_operation">
                    </b-form-input>
                  </b-form-group>
                </b-col>
              </b-row>
            </template>
          </b-form>
      </b-container>
    </b-modal>

    <b-modal 
      id="modalResource2"
      ref="modalResource2"
      :title="`Actualizar ${labelTypeResource}`"
      @ok="onSubmit2"
      @cancel="cancelModal"
      centered>
      <b-container fluid>
          <b-form>
            <b-form-group id='resource_group'
              label="Nombre"
              label-for="resource">
              {{ selectedItem.get_resource_name }}
            </b-form-group>

            <b-row>
              <b-col lg="4">
                <b-form-group id="unit_group"
                  label="Unidad:"
                  label-for="unit">
                  <b-form-input
                    id="unit"
                    type="text"
                    v-model="selectedItem.unit"
                    placeholder="Unidad">
                  </b-form-input>
                </b-form-group>
              </b-col>
              <b-col lg="4">
                <b-form-group id="currency_group"
                  label="Moneda:"
                  label-for="currency">
                  <b-form-select
                    id="currency"
                    v-model="selectedItem.currency">
                    <option value="D">Dólares</option>
                    <option value="S">Soles</option>
                  </b-form-select>
                </b-form-group>
              </b-col>
              <b-col lg="4">
                <b-form-group id="cost_group"
                  v-if="typeResource!='manpower'"
                  label="Costo unitario:"
                  label-for="price">
                  <b-form-input
                    id="price"
                    type="number"
                    step=".1"
                    v-model="selectedItem.price"
                    placeholder="Precio">
                  </b-form-input>
                </b-form-group>
              </b-col>
            </b-row>
            <template v-if="typeResource=='manpower'">
              <b-row>
                <b-col lg="4">
                  <b-form-group id="epp_cost_group"
                    label="Costo EPP:"
                    label-for="epp_cost">
                    <b-form-input
                      id="epp_cost"
                      type="number"
                      step=".01"
                      v-model="selectedItem.epp_cost"
                      placeholder="Costo EPP">
                    </b-form-input>
                  </b-form-group>
                </b-col>
                <b-col lg="4">
                  <b-form-group id="business_cost_group"
                    label="Costo Empresarial:"
                    label-for="business_cost">
                    <b-form-input
                      id="business_cost"
                      type="number"
                      step=".01"
                      v-model="selectedItem.business_cost"
                      placeholder="Costo Empresarial">
                    </b-form-input>
                  </b-form-group>
                </b-col>
                <b-col lg="4">
                  <b-form-group id="type_cost_group"
                    label="Tipo de costo:"
                    label-for="type_cost">
                    <b-form-select
                      id="type_cost"
                      v-model="selectedItem.type_cost">
                      <option value="D">Directo</option>
                      <option value="I">Indirecto</option>
                    </b-form-select>
                  </b-form-group>
                </b-col>
              </b-row>
            </template>
            <template v-if="typeResource=='material'">
              <b-row>
                <b-col lg="4">
                  <b-form-group id="type_material_group"
                    label="Tipo de material:"
                    label-for="type_material">
                    <b-form-select
                      id="type_material"
                      v-model="selectedItem.type_material"
                      :options = "filtros">
                    </b-form-select>
                  </b-form-group>
                </b-col>
              </b-row>
            </template>
            <template v-if="typeResource=='equipment'">
              <b-row>
                <b-col lg="4">
                  <b-form-group id="hours_equipment_operation_group"
                    label="Horas de operación por día:"
                    label-for="hours_equipment_operation">
                    <b-form-input
                      id="hours_equipment_operation"
                      type="number"
                      step="0.50"
                      v-model="selectedItem.hours_equipment_operation">
                    </b-form-input>
                  </b-form-group>
                </b-col>
              </b-row>
            </template>
          </b-form>
      </b-container>
    </b-modal>
  </b-row>
</template>

<script>
  const url_api = `/budget/api/budgets/`
  import { mapGetters } from 'vuex'
  import Menu from "./nav/Menu.vue"
  import Title from "../utils/Title.vue"

  export default {
    components: {
        'app-menu': Menu,
        'app-title': Title,
    },
    data(){
      return{
        selectedResource: "",
        resources: [],
        classMaterial: "S",
        form: {
            budget: "",
            unit: "",
            currency: "D",
            price: "",
            epp_cost: "",
            business_cost: "",
            type_cost: "",
            type_material: "",
            hours_equipment_operation: ""
        },
        searchQuery: '',
        filtered_items: [],
        fields: [],
        isEditing: false,
        action: "add",
        filter: null,
        unit: {
          manpower: "Hr",
          material: "Und",
          equipment: "Hr"
        },
        title: "",
        typeResource: "",
        labelTypeResource: "",
        taskId: "",
        budgetId: "",
        selectedItem: "",
        filtros: [
          { value: "S", text: "Estándar"},
          { value: "M", text: "Médico"},
          { value: "W", text: "Taller"},
          { value: "O", text: "Operativo"},
          { value: "V", text: "Varios"},
          { value: "I", text: "Insumo médico"},
          { value: "E", text: "EPP"},
        ]
      }
    },
    created() {
      this.budgetId = this.$route.params.budget
      this.typeResource = this.$route.params.typeResource
      this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
      if(this.$route.query.task){
        this.$store.dispatch('requestTaskInformation', this.$route.query.task)
      }
      // if(this.$route.query.task){
      //   this.taskId = this.$route.query.task
      //   this.getTask()
      // }
    },
    watch: {
      '$route'(to, from){
        this.budgetId = this.$route.params.budget
        this.typeResource = this.$route.params.typeResource
        //this.$store.requestBudgetInformation(this.budgetId)

        this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
        if(this.$route.query.task){
          this.$store.dispatch('requestTaskInformation', this.$route.query.task)
        }
        // this.taskId = this.$route.query.task
        // if(Boolean(this.taskId)) this.task = this.$store.state.selectedTask
      },
      typeResource(value, old_value){
        this.getResourcesBudget()
        this.form.unit = this.unit[value]
        if(value=="material"){
          this.labelTypeResource = "Material"
          this.fields = [
            {key:'get_resource_label', label: 'Nombre', sortable: true},
            {key:'price', label: 'Costo', sortable: true},
            {key:'type_material', label: 'Clase de Material', sortable: true},
            {key:'actions', label: 'Acciones'}
          ]
        }else{
          if(value=="manpower"){
            this.labelTypeResource = "Mano de Obra"
            this.fields = [
              {key:'get_resource_label', label: 'Nombre', sortable: true},
              {key:'get_cost_unit', label: 'Costo hora', sortable: false},
              {key:'epp_cost', label: 'EPP', sortable: false},
              {key:'business_cost', label: 'Costo Empresarial', sortable: false},
              {key:'type_cost', label: 'Tipo de costo', sortable: true},
              {key:'actions', label: 'Acciones'}
            ]
          }else{
            if(value=="subcontract"){
              this.labelTypeResource = "Subcontrato"
              this.fields = [
                {key:'get_resource_label', label: 'Nombre', sortable: true},
                {key:'price', label: 'Costo', sortable: false},
                {key:'actions', label: 'Acciones'}
              ]
            }else{
              this.labelTypeResource = "Equipo"
              this.fields = [
                {key:'get_resource_label', label: 'Nombre', sortable: true},
                {key:'price', label: 'Costo', sortable: false},
                {key:'hours_equipment_operation', label: 'H.Operac.', sortable: false},
                {key:'actions', label: 'Acciones'}
              ]
            }
          }
        }
      },
    },
    computed: {
      ...mapGetters({
        budget: 'budget/getSelectedBudget',
        task: 'getSelectedTask'

      }),
      items(){
        if(Boolean(this.typeResource)){
          const typeResource = this.typeResource.capitalize()
          if(typeResource=="Material"){
            return this.$store.getters[`budget/getFilteredBudget${typeResource}s`](this.classMaterial)
          }
          return this.$store.getters[`budget/getAvailableBudget${typeResource}s`]
        }
        return []
      }
    },
    methods: {
      showModal(){
        this.$refs.modalResource.show()
      },
      cancelModal(){
        this.$refs.modalResource.hide()
      },
      onFilterClass(){
        //console.log(this.classMaterial)
        this.getResourcesBudget()
      },
      getTask() {
        let url = `/budget/api/tasks/${this.taskId}/`
        this.$http.get(url)
          .then((response) => {
            this.task = response.data
          })
          .catch((err) => {
            console.log('error en getTasks: ', err)
          })
      },
      onEditItem(item){
        console.log('Editar recurso de presupuesto...', item)
        this.isEditing = true
        this.selectedItem = Object.assign({}, item)
        this.$refs.modalResource2.show()
      },
      onSaveItem(item){
        this.isEditing = false
      },
      onCancelItem(item){
        this.isEditing = false
      },
      onResourcesSearch (search, loading) {
        loading(true);
        this.getResources(search, loading)
      },
      getResources(search, loading) {
        let url = `/resource/api/${this.typeResource}/?search=${search}`
        this.$http.get(url)
          .then((response) => {
            this.resources = response.data.results
            // console.log("resources: ", this.resources)
            loading(false)
          })
          .catch((err) => {
            console.log('error getResources::', err);
          })
      },
      getResourcesBudget() {
        if(Boolean(this.typeResource)){
          const typeResource = this.typeResource.capitalize()
          this.$store.dispatch(`budget/requestBudget${typeResource}s`,this.budgetId)
        }
      },
      addItem(){
        let url = `/budget/api/${this.typeResource}_budget/`
        this.form.budget = this.budgetId
        this.$http.post(url, this.form)
          .then((response) => {
            this.getResourcesBudget()
          })
          .catch((err) => {
            console.log(err)
          })
      },
      updateItem(item){
        let url = `/budget/api/${this.typeResource}_budget/${item.id}/`
        this.form.budget = this.budgetId

        this.$http.patch(url, this.form)
        .then((response) => {
            this.getResourcesBudget()
            this.$swal({
              position: 'top-end',
              toast: true,
              type: 'success',
              title: 'Se actualizó correctamente.',
              showConfirmButton: false,
              timer: 1500
            })
          })
          .catch((err) => {
            var msgError
            Object.getOwnPropertyNames(err.body).forEach((element) => {
              msgError += `${element} : ${err.body[element]}\n`
            });
            this.$swal({
              type: 'error',
              title: 'Oops...',
              text: 'Error, no se pudo guardar\n' + msgError
            })
          })
      },
      updateItem2(item){
        let url = `/budget/api/${this.typeResource}_budget/${item.id}/`
        this.selectedItem.budget = this.budgetId

        this.$http.patch(url, this.selectedItem)
        .then((response) => {
            this.getResourcesBudget()
            this.$swal({
              position: 'top-end',
              toast: true,
              type: 'success',
              title: 'Se actualizó correctamente.',
              showConfirmButton: false,
              timer: 1500
            })
          })
          .catch((err) => {
            var msgError
            Object.getOwnPropertyNames(err.body).forEach((element) => {
              msgError += `${element} : ${err.body[element]}\n`
            });
            this.$swal({
              type: 'error',
              title: 'Oops...',
              text: 'Error, no se pudo guardar\n' + msgError
            })
          })
      },
      onChangeValue(e) {
        if (Boolean(e)){
          this.form.unit = e.unit,
          this.form.currency = e.currency,
          this.form.price = e.cost
          this.form[this.typeResource] = e.id
          this.form.epp_cost = e.epp_cost
          this.form.business_cost = e.business_cost
          this.form.type_cost = e.type_cost
          this.form.type_material = e.class_cost
          this.form.hours_equipment_operation = e.hours_equipment_operation
        }
        console.log("change:", this.selectedResource)
      },
      onSubmit2 (evt) {
        evt.preventDefault()
        console.log("selectedItem", this.selectedItem)
        this.updateItem2(this.selectedItem)
        this.$nextTick(() => {
          this.$refs.modalResource2.hide()  
        })
      },
      onSubmit (evt) {
        evt.preventDefault()
        // Si el recurso que se esta tratando de guardar ya existe entonces se actualiza a los recursos de la propuesta.
        let item = this.items.find(item => item[this.typeResource] === this.selectedResource.id)
        // console.log("Item***:", item)
        if (Boolean(item)){
          // console.log("Si exite")
          this.updateItem(item)
        }else{
          // console.log("No existe")
          this.addItem()
        }
        this.$nextTick(() => {
          this.$refs.modalResource.hide()  
        })
        // console.log("item: ", item, evt)
        // if (this.action == 'edit'){
        //   this.updateItem()
        // }else{
        //   this.addItem()
        // }
      },
      onRemoveItem(idx){
        let vm = this
        this.$dialog.confirm(`Desea quitar el recurso ${idx.get_resource_label}`, {
          loader: true
        })
          .then((dialog) => {
            let url=`/budget/api/${this.typeResource}_budget/${idx.id}/`
            this.$http.delete(url)
              .then((response) => {
                this.getResourcesBudget()
                dialog.close()
              })
              .catch((err) => {
                console.log(err)
              })
          })
          .catch((err)=> {
            console.log('Clicked on cancel', err)
          })
      },
      onCancel (evt) {
        evt.preventDefault()
        // this.form.unit = "HH",
        // this.form.currency = "D",
        // this.form.price = ""
        // this.form.manpower = ""
        this.$emit('closeResource')
      },
      // onFiltered (filteredItems) {
      //   // Trigger pagination to update the number of buttons/pages due to filtering
      //   this.totalRows = filteredItems.length
      //   this.currentPage = 1
      // }
    }
  }
</script>
