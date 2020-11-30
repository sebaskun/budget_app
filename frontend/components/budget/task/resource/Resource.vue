<template>
  <b-col md="12" class="my-1">
    <section class="view-data">
      <table class="table table-striped">
        <!-- <col width="60"> -->
        <!-- <col width="20%"> -->
        <!-- <col width="20%"> -->
        <thead>
          <tr>
            <th colspan="3"><span class="th-head">{{title}}</span></th>
            <th class="text-right"><span class="th-head">Total</span></th>
            <th class="text-right"><span class="th-head">{{subtotal|currency(budget.currency)}}</span></th>
            <th class="text-right"><b-link @click="addResource" size="sm"><icon name="plus-square"></icon></b-link></th>
          </tr>
          <tr>
            <th>Descripción</th>
            <th class="text-right">Precio</th>
            <th class="text-right">Rendimiento</th>
            <th class="text-right">Cantidad</th>
            <th class="text-right">Subtotal</th>
            <th></th>

          </tr>
        </thead>
        <tbody>

          <tr v-for="(resource, index) in selectedResources"
            :key=index>
            <th>{{resource.get_resource_label}}</th>
            <td class="text-right">{{ resource.get_resource_price|currency(budget.currency) }}</td>
            <td class="text-right">{{ resource.get_efficiency|decimal("0.00") }}</td>
            <td class="text-right">{{ resource.quantity|decimal('0.000') }}</td>
            <td class="text-right">{{ resource.get_subtotal|currency(budget.currency) }}</td>
            <td class="text-right">
              <b-link @click="editResource(resource)"><icon name="pencil"></icon></b-link>
              <b-link @click="deleteResource(resource)"><icon name="trash"></icon></b-link>
            </td>
          </tr>
          <tr v-if="typeResource=='equipment'">
            <th>Herramientas menores</th>
            <td class="text-right">{{subtotalManpower | currency(budget.currency)}}</td>
            <td class="text-right">{{ 1|decimal('0.000') }}</td>
            <td class="text-right">{{ task.percentage_minor_tools|decimal("0.00%") }}</td>
            <td class="text-right">{{ minorTools|currency(budget.currency) }}</td>
            <td class="text-right"></td>
          </tr>
        </tbody>
      </table>
    </section>
    <!-- Inicio del Modal -->
    <b-modal 
      id="modalForm"
      ref="modalForm"
      :title="`${mode=='add' ? 'Adicionar': 'Actualizar'} ${title}`"
      @ok="onSubmit"
      @cancel="cancelModal"
      centered>
      <b-container fluid>
        <b-form-group id='resource_group'
              label="Recurso">
              <v-select v-if="mode=='add'"
                        id="resource"
                        @input="onChangeValue"
                        v-model="selectedResource"
                        @search="onResourceSearch"
                        :options="resources"
                        label="get_resource_label">
                  <template slot="option" slot-scope="option">
                  <div>
                    {{ `${option.get_resource_code} ${option.get_resource_name} (${option.unit})` }}
                  </div>
                </template>
              </v-select>
              <div v-else>{{model.get_resource_label}}</div>
        </b-form-group>
        <vue-form-generator 
            ref="vfg"
            :schema="schema" 
            :model="model"
            :options="formOptions">
        </vue-form-generator>
      </b-container>
    </b-modal>
    <!-- Fin del Modal -->
  </b-col>
</template>

<script>
  import ResourceList from "./ResourceList.vue"
  import ResourceForm from "./ResourceForm.vue"
  import { mapGetters } from 'vuex'

  export default {
    components: {
      "app-resource-list": ResourceList,
      "app-resource-form": ResourceForm
    },
    props: {
      budget: {type: Object, required: true},
      task: {type: Object, required:true},
      typeResource: {type: String, required: true},
      title: {type: String, required: true},
      subtotalManpower: {default: 0},
      value: {default: 0}
    },
    created() {
      // this.budgetId = this.$route.params.budget
      // this.getBudget()
      // console.log("::created::", this.budgetId)
      this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
      // this.$store.dispatch('budget/requestBudgetPartidas', this.$route.params.budget)
      let tipoRecurso = this.typeResource.capitalize()
      this.$store.dispatch(`${this.typeResource}Partida/requestPartida${tipoRecurso}s`, this.task)
    },
    data(){
      return {
        tipoRecurso: this.typeResource.capitalize(),
        selectedResource: null,
        // fields: [
        //   {key: 'get_resource_label', label: "Recurso"},
        //   {key: 'get_resource_price', label: "Precio"},
        //   {key: 'efficiency', label: "Rendimiento"},
        //   {key: 'quantity', label: "Cantidad"},
        //   {key: 'get_subtotal', label: "Subtotal"}
        // ],
        resourcesTask: [],
        // resources: [],
        subtotal_: 0,
        efficiency: "",
        minorTools: 0,
        model: {},
        mode: "",
        schema: this.getSchema(),
        // schema: {
        //   fields: [
        //     {
        //       type: 'input',
        //       inputType: 'number',
        //       label: 'Cantidad',
        //       model: 'quantity',
        //       required: true,
        //     },
        //     {
        //       type: 'input',
        //       inputType: 'number',
        //       label: 'Rendimiento',
        //       model: 'efficiency',
        //       // required: true,
        //       readonly(){
        //         if(['material', 'subcontract'].includes(this.typeResource)){
        //           console.log("ingresó")
        //           return false
        //         }
        //         return true
        //       },
        //     },
        //   ]
        // },
        formOptions: {
          validateAfterLoad: false,
          validateAfterChanged: false,
          // validateAsync: true
        }
      }
    },
    computed: {
      // ...mapGetters({
      //     budget: 'getSelectedBudget',
      //     task: 'getSelectedTask'
      // }),
      selectedResources() {
        let resources = this.$store.getters[`${this.typeResource}Partida/getAvailablePartida${this.tipoRecurso}s`]
        return resources
      },
      subtotal() {
        let subtotal_ = 0
        console.log("cambio sub total****")
        this.selectedResources.forEach(function(obj){
          subtotal_ += obj.get_subtotal
        })
        if(this.typeResource=='equipment'){
          this.minorTools = this.task.percentage_minor_tools * this.subtotalManpower
          subtotal_ = subtotal_ + this.minorTools
          // console.log("subtotal**", subtotal_)
        }
        // if(this.selectedResources.length==0){
        //   this.$emit('subtotal', 0)
        //   // console.log("sub total tipo:", this.typeResource)
        // }
        this.$emit('input', subtotal_)
        return subtotal_
      },
      resources() {
        return this.$store.getters[`${this.typeResource}Partida/getSearchedPartida${this.tipoRecurso}s`]
      }
    },
    // watch:{
    //   // task(val, oldvalue){
    //   //   console.log(`Actualiza:::${this.typeResource}`)
    //   //   this.updateList()
    //   // },
    //   subtotal(val, oldvalue){
    //     let result = {}
    //     result[this.typeResource] = val
    //     this.$emit('subtotal', val)
    //     this.$emit('input', val)
    //   },
    // },
    methods: {
      getSchema(){
        let readonlyRendimiento = !['material', 'subcontract'].includes(this.typeResource)
        let schema =  {
          fields: [
            {
              type: 'input',
              inputType: 'number',
              label: 'Cantidad',
              model: 'quantity',
              required: true,
            },
            {
              type: 'input',
              inputType: 'number',
              label: 'Rendimiento',
              model: 'efficiency',
              // required: true,
              readonly: readonlyRendimiento,
            },
          ]
        }
        return schema
      },
      isVisibleRendimiento(row){
        // let resources = ["material", "subcontract", "equipment"]
        if(this.typeResource=="material" && row.efficiency!=1){
          return true
        }
        return false
      },
      editEfficiency(){
        return ["material", "subcontract"].includes(this.typeResource) ? true: false
      },
      onChangeValue(e) {
        if (Boolean(e)){
          console.log("Recurso " + this.typeResource, e)
          let fields = ["budget", "currency", this.typeResource, "unit"]
          fields.forEach(elemento=>this.$set(this.model, elemento, e[elemento] ))
          this.$set(this.model, `${this.typeResource}_budget`, e.id )
          console.log("Model " + this.typeResource, this.model)
        }

        // console.log("selected resource", this.selectedResource)
      },
      editResource(index){
        this.mode = "update"
        Object.keys(index).forEach(elemento=>this.$set(this.model, elemento, index[elemento] ))
        this.$refs.modalForm.show()
      },
      onSubmit(evt){
        evt.preventDefault()
        var isValid = this.$refs.vfg.validate()
        
        if(isValid){
          this.$store.dispatch(`${this.typeResource}Partida/${this.mode}Partida${this.tipoRecurso}`, this.model).then(response => {
            this.$swal({
              position: 'top-end',
              toast: true,
              type: 'success',
              title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
              showConfirmButton: false,
              timer: 1500
            })
            // this.$store.dispatch('budget/requestBudgetManpowers', this.$route.params.budget)
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

      },
      onResourceSearch(search, loading) {
        loading(true)
        let q = {search}
        // if(this.typeResource=="material"){
        //   q['']
        // }
        // console.log(q)
        this.$store.dispatch(`${this.typeResource}Partida/searchPartida${this.tipoRecurso}s`, this.budget, q).then(response => {
          // console.log("Hay resultado....")
          loading(false)
        })

      },
      deleteResource(payLoad){
        this.$swal({
          title: `¿Está seguro de eliminar el ${payLoad.get_resource_label}?`,
          type: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Sí, eliminar!'
        })
        .then((willDelete) => {
          if (willDelete.value) {
            // payLoad.is_deleted = true
            this.$store.dispatch(`${this.typeResource}Partida/deletePartida${this.tipoRecurso}`, payLoad)
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
      // deleteResource(index){
      //   console.log("Index:::", index)
      //   let vm = this
      //   this.$dialog.confirm(`Desea quitar el recurso ${index.get_resource_label}`, {
      //     loader: true
      //   })
      //     .then((dialog) => {
      //       let url=`/budget/api/${this.typeResource}_task/${index.id}/`
      //       this.$http.delete(url)
      //         .then((response) => {
      //           vm.updateList()
      //           dialog.close()
      //         })
      //         .catch((err) => {
      //           console.log(err)
      //         })
      //     })
      //     .catch((err)=> {
      //       console.log('Clicked on cancel', err)
      //     })
      // },
      addResource(){
        // this.$set(this.model, "currency", 'S' )
        this.mode = "add"
        this.$set(this.model, "task", this.task.id )
        if(['material', 'subcontract'].includes(this.typeResource)){
          this.$set(this.model, "efficiency", 1)
        }
        this.$refs.modalForm.show()
      },
      // addResource(form){
      //   let url = `/budget/api/${this.typeResource}_task/`
      //   console.log(":::addResource:::", form)
      //   this.$http.post(url, form)
      //     .then((response) => {
      //       this.updateList()
      //     })
      //     .catch((err) => {
      //       console.log(err)
      //     })
      // },
      // editResourceList(form){
      //   let item = this.resourcesTask.find(item => item[this.typeResource] === form[this.typeResource])
      //   if (Boolean(item)){
      //     // Si el elemento ya esta en la lista
      //     form.id = item.id
      //     this.updateResource(form)
      //   }else{
      //     // Si el elemento es nuevo y no esta en la lista
      //     this.addResource(form)
      //   }
      //   this.$store.dispatch('getTaskListByBudget', this.budget.id)
      // },
      // updateResource(form){
      //   let url = `/budget/api/${this.typeResource}_task/${form.id}/`
      //   this.$http.put(url, form)
      //     .then((response) => {
      //       this.updateList()
      //     })
      //     .catch((err) => {
      //       console.log(err)
      //     })
      // },
      updateResource2(form){
        let url = `/budget/api/${this.typeResource}_task/${form.id}/`
        this.$http.put(url, form)
          .then((response) => {
          })
          .catch((err) => {
            console.log(err)
          })
      },
      updateList(){
        let url = `/budget/api/tasks/${this.task.id}/${this.typeResource}s/`
        let vm = this
        this.$http.get(url)
          .then((response) => {
            console.log("+++updateList+++", response.data)
            vm.resourcesTask = response.data
            vm.$store.dispatch('updateTaskInformation', vm.task.id)
          })
          .catch((err) => {
            console.log(err);
          })
      },
      // refreshCosting(){
      //   this.updateList()
      // },
      reCalcEfficiency(new_efficiency){
        let efficiency = new_efficiency
        let vm = this
        let priceResource = 0
        let subtotalTypeResource = 0
        this.resourcesTask.forEach(function(obj){
          if (vm.typeResource!="material"){
            obj.efficiency = parseFloat(8 / efficiency).toFixed(2);
            obj.get_subtotal = obj.efficiency * obj.quantity * obj.get_resource_price
            subtotalTypeResource += obj.get_subtotal
            let form = {
              id: obj.id,
              efficiency: obj.efficiency,
              task: obj.task
            }
            form[vm.typeResource] = obj[vm.typeResource]
            vm.updateResource2(form)
          }
        })
        this.subtotal_ = subtotalTypeResource
      }
    },
    mounted(){
      this.$eventHub.$on('reCalcEfficiency', this.reCalcEfficiency)
      // this.$eventHub.$on('refreshCosting', this.refreshCosting)
    },
    // beforeDestroy() {
    //     this.$eventHub.$off('reCalcEfficiency')
    //     this.$eventHub.$off('refreshCosting')
    // }
  }
</script>

<style>
    /* .resource-list {
        margin-bottom: 40px;
    } */
</style>
