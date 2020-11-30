<template>
  <div style="display: inline-block">
    <b-button size="sm" @click="showModal">Coef. Markup Diferencial</b-button>
    <b-modal id="modalRatioMarkUpDiferenciado"
            ref="modalRatioMarkUpDiferenciado"
            title="Coeficiente de MarkUp Diferenciado"
            size="lg"
            @ok="handleOk"
            @cancel="handleCancel"
            centered>
      <b-container fluid>
      <form>
            <table class="table table-striped">
              <col width="20%">
              <col width="20%">
              <col width="20%">
              <col width="20%">
              <col width="20%">
              <thead>
                <tr>
                  <th>ITEM</th>
                  <th class="text-right">M.O.</th>
                  <th class="text-right">Eq & Her</th>
                  <th class="text-right">Mater.</th>
                  <th class="text-right">Sub.</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>Imprevistos</th>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_incidentals_manpowers'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_incidentals_manpowers">
                    </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_incidentals_equipments'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_incidentals_equipments">
                  </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_incidentals_materials'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_incidentals_materials">
                  </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_incidentals_subcontracts'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_incidentals_subcontracts">
                  </b-form-input></td>
                </tr>
                <tr>
                  <th>Gastos Grales</th>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_over_head_manpowers'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_over_head_manpowers">
                    </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_over_head_equipments'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_over_head_equipments">
                    </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_over_head_materials'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_over_head_materials">
                    </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_over_head_subcontracts'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_over_head_subcontracts">
                    </b-form-input></td>
                </tr>
                <tr>
                  <th>Beneficio</th>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_profit_manpowers'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_profit_manpowers">
                    </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_profit_materials'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_profit_materials">
                    </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_profit_equipments'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_profit_equipments">
                    </b-form-input></td>
                  <td class="text-right">
                    <b-form-input
                      id='ratio_profit_subcontracts'
                      type="number"
                      min="0"
                      step="0.01"
                      v-model="values.ratio_profit_subcontracts">
                    </b-form-input></td>
                </tr>
              </tbody>
            </table>

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
          Object.getOwnPropertyNames(this.values).forEach((element) => {
            this.backForm[element] = this.values[element]
          })
          // this.backForm = JSON.parse(JSON.stringify(this.values))
          this.$refs.modalRatioMarkUpDiferenciado.show()
        },
        handleCancel(evt){
          evt.preventDefault()
          Object.getOwnPropertyNames(this.backForm).forEach((element) => {
            this.values[element] = this.backForm[element]
          })
          // this.values = JSON.parse(JSON.stringify(this.backForm))
          this.$refs.modalRatioMarkUpDiferenciado.hide()
        },
        handleOk (evt) {
          // Controla que los datos sean válidos
          evt.preventDefault()
          if (!Number(this.values.ratio_incidentals_manpowers)>0 ||
              !Number(this.values.ratio_incidentals_equipments)>0 ||
              !Number(this.values.ratio_incidentals_materials)>0 ||
              !Number(this.values.ratio_incidentals_subcontracts)>0 ||
              !Number(this.values.ratio_over_head_manpowers)>0 ||
              !Number(this.values.ratio_over_head_materials)>0 ||
              !Number(this.values.ratio_over_head_equipments)>0 ||
              !Number(this.values.ratio_over_head_subcontracts)>0 ||
              !Number(this.values.ratio_profit_manpowers)>0 ||
              !Number(this.values.ratio_profit_materials)>0 ||
              !Number(this.values.ratio_profit_equipments)>0 ||
              !Number(this.values.ratio_profit_subcontracts)>0){
              alert('Los valores deben ser positivos')
          } else {
            this.handleSubmit()
          }
        },
        handleSubmit () {
          // console.log("handleSubmit::", this.values)
          this.$emit("onSave", this.values)
          this.$refs.modalRatioMarkUpDiferenciado.hide()
        },
      },
  }
</script>
