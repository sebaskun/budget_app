<template>
  <div>
    <div class="content-apu" v-if="task">
      <b-link @click="onEdit()" id="popover-partida"><h6>{{getTitlePartida()}}</h6></b-link>
    </div>
    <b-modal 
      id="modalForm"
      ref="modalForm"
      title="Editar"
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
  </div>
</template>

<script>
  var _ = require('lodash')
  import { mapGetters } from 'vuex'

  export default {
    props:{
      task: {type: Object, required:true}
    },
    data() {
      return {
        popoverShow: false,
        editTask: false,
        textEdit: "Editar",
        formEfficiency: {
          efficiency: null,
          efficiency_divider: null
        },
        draft: {},
        model: {},
        schema: {
          fields: [
            {
              type: 'input',
              inputType: 'text',
              label: 'Nombre partida',
              model: 'name',
              required: true,
            },
            {
              type: 'input',
              inputType: 'text',
              label: 'Unidad',
              model: 'unit',
              required: false,
            },
            {
              type: 'input',
              inputType: 'text',
              label: 'EDT',
              model: 'wbs',
              required: false,
            },
            {
              type: 'input',
              inputType: 'number',
              label: 'Rendimiento',
              model: 'efficiency',
              required: false,
            },
            {
              type: 'input',
              inputType: 'number',
              label: 'Cantidad',
              model: 'quantity',
              required: false,
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
    computed: {
      ...mapGetters({
          budget: 'getSelectedBudget',
      }),
      efficiencyComputed(){
        if(this.formEfficiency.efficiency_divider > 0){
          return this.formEfficiency.efficiency / this.formEfficiency.efficiency_divider
        }
        return this.formEfficiency.efficiency
      }
    },
    watch: {
    },
    methods: {
      getTitlePartida(){
        return `${this.task.wbs ? this.task.wbs: ''} ${this.task.name} ${this.task.unit ? '(' + this.task.unit + ')' : ''}`
      },
      onEdit(){
        Object.keys(this.task).forEach(elemento=>this.$set(this.model, elemento, this.task[elemento] ))
        this.$refs.modalForm.show()
      },
      cancelModal(){
        console.log("Cierra el modal")
        this.$refs.modalForm.hide()
      },
      onClose(){
        this.popoverShow = false
      },
      onSubmit(evt){
        evt.preventDefault()
        var isValid = this.$refs.vfg.validate()
        if(isValid){
          this.$store.dispatch(`budget/updateBudgetPartida`, this.model).then(response => {
            this.$swal({
              position: 'top-end',
              toast: true,
              type: 'success',
              title: `Se actualizó correctamente.`,
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
    }
  }
</script>
