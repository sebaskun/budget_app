<template>
  <div style="display: inline-block">
    <b-button size="sm" @click="showModal">Coef. de paso</b-button>
    <b-modal id="modalRatioBudget"
            ref="modalForm"
            title="Coeficiente de paso"
            @ok="handleOk"
            centered>
      <b-container fluid>
      <form>
        <b-row class="mb-1">
          <b-col cols="3">Mano de obra</b-col>
          <b-col><b-form-input type="number" v-model="values.ratio_manpower"></b-form-input></b-col>
        </b-row>
        <b-row class="mb-1">
          <b-col cols="3">Material</b-col>
          <b-col><b-form-input type="number" v-model="values.ratio_material"></b-form-input></b-col>
        </b-row>
        <b-row class="mb-1">
          <b-col cols="3">Equipo</b-col>
          <b-col><b-form-input type="number" v-model="values.ratio_equipment"></b-form-input></b-col>
        </b-row>
        <b-row class="mb-1">
          <b-col cols="3">Sub contrato</b-col>
          <b-col><b-form-input type="number" v-model="values.ratio_subcontract"></b-form-input></b-col>
        </b-row>
      </form>
      </b-container>
    </b-modal>
  </div>
</template>

<script>
  export default {
      props:{
        values: {
          required: true,
          type: Object,
        }
      },
      data() {
        return {
          editingScheduledCompletion: false,
          backForm: {}
        }
      },
      methods: {
        showModal(){
          this.backForm = JSON.parse(JSON.stringify(this.values))
          this.$refs.modalForm.show()
        },
        handleCancel(evt){
          evt.preventDefault()
          this.values = JSON.parse(JSON.stringify(this.backForm))
          this.$refs.modalForm.hide()
        },
        handleOk (evt) {
          // Controla que los datos sean válidos
          evt.preventDefault()
          if (!this.values.ratio_manpower || !Number(this.values.ratio_manpower)>0) {
            alert('Ingrese un coeficiente para mano de obra')
          } else if(!this.values.ratio_material || !Number(this.values.ratio_material)>0) {
            alert('Ingrese un coeficiente para material')
          } else if(!this.values.ratio_equipment || !Number(this.values.ratio_equipment)>0) {
            alert('Ingrese un coeficiente para equipo')
          } else if(!this.values.ratio_subcontract || !Number(this.values.ratio_subcontract)>0) {
            alert('Ingrese un coeficiente para sub contrato')
          } else {

            this.handleSubmit()
          }
        },
        handleSubmit () {
          // console.log("handleSubmit::", this.values)
          this.$refs.modalForm.hide()
          this.$emit("onSave", this.values)
        },
      },
  }
</script>
