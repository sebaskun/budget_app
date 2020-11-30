<template>
  <b-row>
      <div class="bd-content">
        <b-container fluid>
            <vue-form-generator 
                ref="vfg"
                :schema="schema" 
                :model="model"
                :options="formOptions">
            </vue-form-generator>
            <!-- <b-button variant="primary" size="sm" @click="onSubmit">Aceptar</b-button> -->
            <p> </p>
        </b-container>
      </div>
      <!-- {{budget}} -->
  </b-row>
</template>

<script>

// import filter from 'lodash/filter'
// import HandleItem from "./budget/HandleBudget.vue"
// import { mapGetters } from 'vuex'
// import '../utils/icons/042-add'
// const url_api = '/budget/api/budgets/'
var numeral = require("numeral")

export default {
    data() {
        return {
          title: "Presupuesto",
          model: {},
          filter: "",
          vacunas: [],
          currentPage: 1,
            schema: {
              groups: [
                {
                    legend: "Datos Generales",
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
                      {
                        type: "submit",
                        inputType: "submit",
                        buttonText: "Enviar",
                        onSubmit: this.onSubmit,
                        validateBeforeSubmit: true
                      },
                    ]
                },
                {
                    legend: "Coeficiente de paso",
                    fields: [
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Mano de obra',
                        model: 'ratio_manpower',
                        required: true,
                        // validator: ['number']
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Material',
                        model: 'ratio_material',
                        required: true,
                        // validator: ['number']
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Equipo',
                        model: 'ratio_equipment',
                        required: true,
                        // validator: ['number']
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Subcontrato',
                        model: 'ratio_subcontract',
                        required: true,
                        // validator: ['number']
                      },
                      {
                        type: "submit",
                        inputType: "submit",
                        buttonText: "Enviar",
                        onSubmit: this.onSubmit,
                        validateBeforeSubmit: true
                      },
                    ]
                },
                { 
                  legend: "Costos Médicos",
                  fields: [ 
                      {
                        type: 'select',
                        label: 'Vacuna',
                        model: 'vacunas',
                        required: false,
                        values(){
                            var vacunas = this.$store.getters['vacuna/getVacunas']
                            // console.log("ubicaciones:", ubicaciones)
                            return vacunas.map((e)=>{return {id: e.id, name: e.nombre, costo: e.get_costo_vacuna}})
                        },
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Costo de Vacunación (S/)',
                        model: 'vacuna_costo',
                        readonly: true,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Amortización (meses)',
                        model: 'meses_obra',
                        required: false,
                      },
                      {
                        type: "input",
                        inputType: "text",
                        label: "Vacunación (por mes)",
                        model: "get_costo_vacunacion",
                        readonly: true,
                        //   featured: false,
                        //   disabled: true
                      },
                      {
                        type: "input",
                        inputType: "number",
                        label: "Exámen médico pre-ocupacional",
                        model: "costo_examen_medico_pre_ocupacional",
                        //   featured: false,
                        //   disabled: true
                      },
                      {
                        type: "input",
                        inputType: "number",
                        label: "Exámen médico post-ocupacional",
                        model: "costo_examen_medico_post_ocupacional",
                        //   featured: false,
                        //   disabled: true
                      },
                      {
                        type: "submit",
                        inputType: "submit",
                        buttonText: "Enviar",
                        onSubmit: this.onSubmit,
                        validateBeforeSubmit: true
                      },
                    ]
                },
                { 
                    legend: "EPP",
                    fields: [ 
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Amortización (meses)',
                        model: 'meses_epp',
                        required: false,
                      },
                    ]
                },
                { 
                    legend: "Certificación",
                    fields: [ 
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Amortización certificación (meses)',
                        model: 'meses_costo_certificacion',
                        required: false,
                      }
                    ]
                },
                {
                    legend: "Otros costos",
                    fields: [ 
                      {
                        type: 'input',
                        inputType: 'text',
                        label: 'Nombre Gasto 1',
                        model: 'nombre_gasto_1',
                        required: false,
                      },
                      {
                        type: 'select',
                        label: 'Moneda Gasto 1',
                        model: 'moneda_gasto_1',
                        required: false,
                        values(){
                            return [
                                { id: "S", name: "Soles" },
                                { id: "D", name: "Dólares" }
                            ]
                            },
                        validator: ['string'],
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Costo gasto 1',
                        model: 'costo_gasto_1',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Veces gasto 1',
                        model: 'veces_gasto_1',
                        required: false,
                      },
                      {
                        type: "submit",
                        inputType: "submit",
                        buttonText: "Enviar",
                        onSubmit: this.onSubmit,
                        validateBeforeSubmit: true
                      },
                    ]
                },
                { 
                    legend: "Catering Hotelería",
                    fields: [
                      {
                        type: 'select',
                        label: 'Moneda',
                        model: 'catering_hoteleria_moneda',
                        required: false,
                        values(){
                            return [
                                { id: "S", name: "Soles" },
                                { id: "D", name: "Dólares" }
                            ]
                            },
                        validator: ['string'],
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Costo',
                        model: 'catering_hoteleria_costo',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Días',
                        model: 'catering_hoteleria_dias',
                        required: false,
                      },
                      {
                        type: "submit",
                        inputType: "submit",
                        buttonText: "Enviar",
                        onSubmit: this.onSubmit,
                        validateBeforeSubmit: true
                      },
                    ]
                },
                { 
                    legend: "Medicina",
                    fields: [ 
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Días medicina',
                        model: 'medicina_dias',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'text',
                        label: 'Costo',
                        model: 'medicina_costo',
                        required: false,
                      },
                      {
                        type: 'select',
                        label: 'Moneda',
                        model: 'medicina_moneda',
                        required: false,
                        values(){
                            return [
                                { id: "S", name: "Soles" },
                                { id: "D", name: "Dólares" }
                            ]
                            },
                        validator: ['string'],
                      },
                      {
                        type: "submit",
                        inputType: "submit",
                        buttonText: "Enviar",
                        onSubmit: this.onSubmit,
                        validateBeforeSubmit: true
                      },
                    ]
                },
                { 
                    legend: "Equipo",
                    fields: [ 
                      {
                        type: 'input',
                        inputType: 'number',
                        label: '% Reparación y reposición',
                        model: 'ratio_equipo_reparacion_reposicion',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Precio gasoil (US$)',
                        model: 'precio_gasoil',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Precio gasolina (US$)',
                        model: 'precio_gasolina',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Consumo equipo',
                        model: 'ratio_consumo_equipos',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: '% Lubricante',
                        model: 'ratio_lubricante',
                        required: false,
                      },
                      {
                        type: "switch",
                        label: "¿Cliente asume combustible?",
                        model: "is_cliente_asume_combustible",
                        textOn: "Asume",
                        textOff: "No asume"
                      },
                      {
                        type: "submit",
                        inputType: "submit",
                        buttonText: "Enviar",
                        onSubmit: this.onSubmit,
                        validateBeforeSubmit: true
                      },
                    ]
                },
                { 
                    legend: "Obligaciones legales",
                    fields: [ 
                      {
                        type: 'input',
                        inputType: 'number',
                        label: '% Gratificación julio y diciembre',
                        model: 'ratio_manpower_gratificacion_julio_diciembre',
                        required: false,
                      },
                      {
                        type: 'label',
                        // inputType: 'number',
                        label: '% Gratificación julio y diciembre',
                        model: 'get_gratificacion',
                        get: function(model) {
                          return numeral(model.get_gratificacion).format("0,0.00%")
                        }
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: '% Vacaciones truncas',
                        model: 'ratio_vacaciones_truncas',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: 'Es Salud',
                        model: 'ratio_es_salud',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: '% SCTR SALUD',
                        model: 'ratio_sctr_salud',
                        required: false,
                      },
                      {
                        type: 'input',
                        inputType: 'number',
                        label: '% SCTR PENSIÓN',
                        model: 'ratio_sctr_pension',
                        required: false,
                      },
                      {
                        type: "submit",
                        inputType: "submit",
                        buttonText: "Enviar",
                        onSubmit: this.onSubmit,
                        validateBeforeSubmit: true
                      },
                    ]
                },
              ]
            },
            formOptions: {
              validateAfterLoad: false,
              validateAfterChanged: false,
            }
        }
    },
    computed: {
      budget(){
        let data = this.$store.getters['budget/getSelectedBudget']
        // console.log("data>>>", data)
        
        // console.log("Model>>>", this.model)
        return data
      },
    },
    mounted(){
      this.$store.dispatch('client/requestClients')
      this.$store.dispatch('grupo/requestAvailableListGrupo')
      this.$store.dispatch('vacuna/requestAvailableListVacunas')
      this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
    },
    watch: {
      budget (to, from) {
        Object.keys(to).forEach(elemento=>this.$set(this.model, elemento, to[elemento] ))
      },
      "model.vacunas"(to, from){
        // console.log("vacuna:", to)
        if(to==null) this.$set(this.model, "vacuna_costo", '0.00')
        if(this.model.vacuna_costo==0){
          let vacuna = this.$store.getters["vacuna/getFilteredVacuna"](to)
          if (vacuna[0]){
            // if(this.budget.currency == "D"){
            //   this.$set(this.budget, "vacuna_costo", vacuna[0].get_costo_vacuna / this.budget.exchange_rate)
            // }
            this.$set(this.model, "vacuna_costo", vacuna[0].get_costo_vacuna)
          }
        }
      },
    },
    methods: {
      onSubmit(evt){
        // console.log("evt:", evt)
        // evt.preventDefault()
        var isValid = this.$refs.vfg.validate()
        if(isValid){
          this.$store.dispatch(`budget/updateBudget`, this.model).then(response => {
            this.$swal({
              position: 'top-end',
              toast: true,
              type: 'success',
              title: `Se actualizó correctamente.`,
              showConfirmButton: false,
              timer: 1500
            })
            // this.$store.dispatch('budget/requestBudgetInformation', this.budget.id)
            // this.$store.dispatch('budget/requestBudgetInformation', this.budget.id)
            // this.$refs.modalForm.hide()
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
    }
  }
</script>
