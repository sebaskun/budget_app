<template>
  <div>
    <div v-if="isLoading">
        <div>Loading...</div>
    </div>
    <b-alert :show="shouldShowPositiveMessage"
             dismissible
             fade
             variant="primary">
      Presupuesto {{ this.isCreatingNewRecord ? 'creado' : 'actualizado' }} correctamente.
    </b-alert>
    <b-alert :show="shouldShowNegativeMessage"
             dismissible
             fade
             variant="warning">
      <div class="header">{{ error.type | startCase }}</div>
      <p>{{ error.title }}</p>
    </b-alert>

    <div>
      <b-form-group id="title_group"
            label="Titulo:"
            label-for="title"
            description="Escriba el título completo del presupuesto.">
            <b-form-textarea
              v-if="isEditing"
              id="title"
              v-model="budget.title"
              placeholder="Titulo del presupuesto"
              :rows="3"
              :max-rows="6">
            </b-form-textarea>
            <div v-else>{{budget.title}}</div>
      </b-form-group>
      <b-form-group id="client_group"
            label="Cliente:"
            label-for="client"
            description="Escriba el nombre del cliente">
            <v-select
              v-if="isEditing"
              id="client"
              v-model="selectedClient"
              :options="clients"
              label="name">
            </v-select>
            <div v-else>{{budget.get_client}}</div>
      </b-form-group>

      <b-row>
        <b-col lg="4">
          <b-form-group id="exchange_rate_group"
            label="Tipo de cambio:"
            label-for="exchange_rate"
            description="Escriba el tipo de cambio">
            <b-form-input
              v-if="isEditing"
              id="exchange_rate"
              type="number"
              step=".1"
              v-model="budget.exchange_rate"
              placeholder="Tipo de cambio">
            </b-form-input>
            <div v-else>{{budget.exchange_rate}}</div>
          </b-form-group>
        </b-col>
        <b-col lg="4">
          <b-form-group id="currency_group"
            label="Moneda:"
            label-for="currency">
            <b-form-select
              v-if="isEditing"
              id="currency"
              v-model="budget.currency">
              <option selected value="D">Dólares</option>
              <option value="S">Soles</option>
            </b-form-select>
            <div v-else>{{budget.currency}}</div>
          </b-form-group>
        </b-col>
        <b-col lg="4">
          <b-form-group id="deadline_group"
            label="F.Presentación"
            label-for="deadline">
            <b-form-input
              v-if="isEditing"
              id="deadline"
              type="date"
              v-model="budget.deadline">
            </b-form-input>
            <div v-else>{{budget.deadline}}</div>
          </b-form-group>
        </b-col>
      </b-row>
      <b-form-group id="location_group"
            label="Locación"
            description="Escriba la ubicación del proyecto">
            <b-form-input
              v-if="isEditing"
              id="location"
              type="text"
              maxlength="150"
              placeholder="Escriba la locación del presupuesto"
              v-model="budget.location">
            </b-form-input>
            <div v-else>{{budget.location}}</div>
      </b-form-group>
      <b-button @click="onPrimaryButtonClick" variant="primary">{{primaryButtonLabel}}</b-button>
      <b-button @click="onCancelButtonClick" variant="danger">Cancelar</b-button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import map from 'lodash/map'
import lodashStartCase from 'lodash/startCase'
export default {
    props: {
        budget: {
            required: true,
            type: Object
        },
        isCreatingNewRecord: {
            required: true,
            type: Boolean
        }
    },
    data() {
        return {
            error: {},
            isEditing: false,
            isLoading: false,
            selectedManufacturerId: null,
            shouldShowPositiveMessage: false,
            shouldShowNegativeMessage: false,
            selectedClient: null,
            dismissCountDown: 5,
        }
    },
    computed: {
      ...mapGetters({
          clientsList: 'getAvailableClients'
      }),
      clients(){
        // return this.clientsList.results
        return map(this.clientsList.results, client => {
                return {
                    name: client.name,
                    // text: client.name,
                    value: client.id
                }
        })
      },
      primaryButtonLabel() {
          return this.isEditing ? 'Guardar' : 'Modificar';
      },
    },
    filters: {
        startCase(value) {
            return lodashStartCase(value);
        }
    },
    created() {
      if (this.isCreatingNewRecord) {
        this.isEditing = true;
      }
      console.log("::::created:::")
    },
    methods: {
      onPrimaryButtonClick() {
        if (!this.isEditing) {
            this.isEditing = true
            this.selectedClient = this.clients.find(item => item.value === this.budget.client)
            return
        }
        this.isLoading = true;
        const payload = {
            title: this.budget.title,
            exchange_rate: this.budget.exchange_rate,
            currency: this.budget.currency,
            deadline: this.budget.deadline || null,
            location: this.budget.location || null,
            summary: this.budget.summary || null,
            client: this.selectedClient.value,
        }
        // if (this.isCreatingNewRecord) {
        //     payload.title = this.budget.title;
        // }
        const errorHandler = error => {
            this.error = error.body
            this.shouldShowNegativeMessage = true
            this.isLoading = false
        };
        if (this.isCreatingNewRecord) {
            this.$http.post('budget/api/budgets/', payload).then(() => {
                this.shouldShowPositiveMessage = true
                this.$store.dispatch('requestBudgetList')
                this.$emit('newBudgetAdded');
                this.isLoading = false
            }, errorHandler)
        } else if (this.isEditing) {
            this.$http.patch(`budget/api/budgets/${this.budget.id}/`, payload).then(() => {
                this.isEditing = false
                this.shouldShowPositiveMessage = true
                this.$store.dispatch('updateBudgetInformation', this.budget.id)
                this.isLoading = false
            }, errorHandler)
        }
      },
      onCancelButtonClick() {
          this.resetInitialState();
          this.$emit('cancelButtonClicked');
      },
      resetInitialState() {
          this.error = null;
          this.isEditing = false;
          this.selectedManufacturerId = null;
          this.shouldShowPositiveMessage = false;
          this.shouldShowNegativeMessage = false;
      },
    }
}
</script>
