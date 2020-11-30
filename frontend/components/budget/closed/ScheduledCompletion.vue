<template>
  <!-- Plazo de obra -->
  <b-col md="12" class="my-1">
    <section class="view-data">
      <table class="table table-striped">
        <col width="35%">
        <col width="10%">
        <col width="5%">
        <col width="40%">
        <col width="10%">
        <tbody>
          <tr>
              <th>PLAZO DE OBRA</th>
              <td class="text-right">
                <template v-if="!editingScheduledCompletion">
                  {{scheduledCompletion.scheduled_completion|decimal}} meses
                </template>
                <template v-else>
                  <b-form-input
                    id='scheduled_completion'
                    type="number"
                    min="0"
                    step="1"
                    v-model="scheduledCompletion.scheduled_completion">
                  </b-form-input>
                </template>
              </td>
              <td class="text-right">
                <template v-if="!editingScheduledCompletion">
                  <a @click="editScheduledCompletion()">
                      <icon name="pencil"></icon>
                  </a>
                </template>
                <template v-else>
                  <a @click="saveScheduledCompletion()">
                      <icon name="check"></icon>
                  </a>
                  <a @click="cancelScheduledCompletion()">
                      <icon name="times"></icon>
                  </a>
                </template>
              </td>

              <th>PLAZO DE FIEL CUMPLIMIENTO</th>
              <td class="text-right">
                <b-btn @click="showModal" size="sm" variant="outline-primary">{{ scheduledCompletion.get_period_faithful_compliance + " meses" }}</b-btn>
              </td>
              <td class="text-right">

              </td>
          </tr>
        </tbody>
      </table>
    </section>
    <b-modal id="modalScheduledCompletion"
            ref="modalScheduledCompletion"
            title="Plazo de fiel cumplimiento"
            @ok="handleScheduledCompletionOk"
            @cancel="handleScheduledCompletionCancel"
            centered>
      <b-container fluid>
      <form>
        <b-row class="mb-1">
          <b-col cols="3">Plazo de fiel cumplimiento</b-col>
          <b-col>{{getPeriodFaithfulCompliance}}</b-col>
        </b-row>
        <b-row class="mb-1">
          <b-col cols="3">Tiempo adicional</b-col>
          <b-col><b-form-input type="number" min="0" step="1" v-model="scheduledCompletion.scheduled_completion_extra"></b-form-input></b-col>
        </b-row>
      </form>
      </b-container>
    </b-modal>
  </b-col>
  <!-- Fin: Costo indirecto -->
</template>

<script>

  const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }

  export default {
      props:{
        scheduledCompletion: {
          required: true,
          type: Object,
        }
      },
      data() {
        return {
          editingScheduledCompletion: false,
          backScheduledCompletion: {
            scheduled_completion: "",
            scheduled_completion_extra: ""
          }
        }
      },
      computed:{
        getPeriodFaithfulCompliance(){
          let total = 0
          if (this.scheduledCompletion){
            total = Number(this.scheduledCompletion.scheduled_completion) + Number(this.scheduledCompletion.scheduled_completion_extra)
          }
          return total
        },
      },
      methods: {
        showModal(){
          this.backScheduledCompletion.scheduled_completion_extra = this.scheduledCompletion.scheduled_completion_extra
          this.$refs.modalScheduledCompletion.show()
        },
        cancelScheduledCompletion(){
          this.scheduledCompletion.scheduled_completion = this.backScheduledCompletion.scheduled_completion
          this.editingScheduledCompletion = false
        },
        saveScheduledCompletion(){
          this.$emit("onSaveScheduledCompletion", {scheduled_completion: this.scheduledCompletion.scheduled_completion})
          this.editingScheduledCompletion = false
        },
        editScheduledCompletion(){
          this.backScheduledCompletion.scheduled_completion = this.scheduledCompletion.scheduled_completion
          this.editingScheduledCompletion = true
        },
        handleScheduledCompletionCancel(evt){
          evt.preventDefault()
          this.scheduledCompletion.scheduled_completion_extra = this.backScheduledCompletion.scheduled_completion_extra
          this.$refs.modalScheduledCompletion.hide()
        },
        handleScheduledCompletionOk (evt) {
          // Controla que los datos sean válidos
          evt.preventDefault()
          if (!Number(this.scheduledCompletion.scheduled_completion_extra>=0)){
            alert('Ingrese un número positivo')
          } else {
            this.handleScheduledCompletionSubmit()
          }
        },
        handleScheduledCompletionSubmit () {
          this.$emit("onSaveScheduledCompletion", {scheduled_completion_extra: this.scheduledCompletion.scheduled_completion_extra})
          this.$refs.modalScheduledCompletion.hide()
        },
      },
  }
</script>
