<template>
  <b-row>
    <b-col md="8">
      <b-row class="bd-title">
        <h5>Config. Gastos Generales</h5>
      </b-row>
      <b-row class="bd-content">

          <b-col md="12" class="my-1">
            <b-form-group horizontal label="Filtro" class="mb-0">
              <b-input-group>
                <b-form-input v-model="searchQuery" placeholder="Escriba para buscar" />
                <b-input-group-append>
                  <b-btn :disabled="!searchQuery" @click="searchQuery = ''">Limpiar</b-btn>
                </b-input-group-append>
              </b-input-group>
            </b-form-group>
            <b-table
              striped hover :items="filteredOverHeads" :fields="fields"
              :filter="filter" @filtered="onFiltered">
              <template slot="actions" slot-scope="row">
                  <b-button size="sm" @click="onBudgetItemClick(row.item)" class="mr-1">Editar</b-button>
                  <b-button size="sm" @click="onGoToCost(row.item.id)" class="mr-1">Costo</b-button>
              </template>
              <template slot="image" slot-scope="row"><img :src="row.item.get_image_miniature_50_0" alt=""></template>
              <template slot="row-details" slot-scope="row">
                  <b-card>
                      <p>{{row.item.description}}</p>

                  </b-card>
              </template>
            </b-table>
          </b-col>
        </b-row>
    </b-col>
    <b-col md="4">
      <b-row class="bd-content">
        <b-col md="12" class="my-1">
          <app-handle-item
            v-if="shouldShowForm"
            :budget="selectedBudget"
            :isCreatingNewRecord="isCreatingNewRecord"
            @newBudgetAdded="onNewBudgetAdded"
            @cancelButtonClicked="onCancelButtonClicked"></app-handle-item>
          <div v-else>
            <p>Por favor seleccione un item de la lista de la izquierda para ver su información.</p>
            <p>Puede usar el botón de abajo para crear un presupuesto nuevo.</p>
            <button class="ui olive right labeled icon button" @click="onAddButtonClick">
                <i class="plus icon"></i>
                Adicionar presupuesto
            </button>
          </div>
        </b-col>
      </b-row>
    </b-col>
  </b-row>
</template>

<script>

import filter from 'lodash/filter'
import HandleItem from "./setting/FormOverHead.vue"
import { mapGetters } from 'vuex'

// const url_api = '/budget/api/budgets/'

export default {
    components: {
        'app-handle-item': HandleItem,
    },
    data() {
        return {
          selectedBudget: null,
          searchQuery: '',
          title: "Presupuesto",
          handleTitle: "",
          filtered_items: [],
          items: [],
          fields: [
              {key:'image', label: 'Logo'},
              {key:'get_client', label: 'Cliente', sortable: true},
              {key:'code', label: 'Código', sortable: true},
              {key:'title', label: 'Título', sortable: true},
              {key:'location', label: 'Locación', sortable: true},
              {key:'actions', label: 'Acciones'}],
          isEditing: false,
          action: "add",
          filter: null,
          id: ""
        }
    },
    computed: {
      ...mapGetters({
          budgets: 'getAvailableBudgets',
      }),
      shouldShowForm() {
          return this.selectedBudget !== null;
      },
      filteredBudgets() {
        return filter(this.budgets.results, (item) => {
            const hasBudgetMatch = (item.title.toLowerCase().indexOf(this.searchQuery) !== -1);
            // const hasManufacturerMatch = (item._embedded.manufacturer.name.toLowerCase().indexOf(this.searchQuery) !== -1);
            return hasBudgetMatch  // || hasManufacturerMatch;
        });
      },
    },
    methods: {
      onGoToCost(budget){
        this.$store.dispatch('requestBudgetInformation', budget)
        this.$router.push({name: 'budget-costing', params: {budget}})
      },
      onAddButtonClick() {
          this.isCreatingNewRecord = true;
          this.selectedBudget = {
            title: "",
            exchange_rate: "",
            currency: "D",
            deadline: "",
            location: "",
            summary: "",
            client: ""
          };
      },
      onCancelButtonClicked() {
          this.isCreatingNewRecord = false;
          this.selectedBudget = null;
      },
      onBudgetItemClick(budget) {
          this.isCreatingNewRecord = false;
          (this.selectedBudget === budget) ? this.selectedBudget = null : this.selectedBudget = budget;
      },
      onNewBudgetAdded() {
          this.selectedBudget = {
            title: "",
            exchange_rate: "",
            currency: "D",
            deadline: "",
            location: "",
            summary: "",
            client: "",
        }
      },
      onCostItem(index) {
        this.isEditing = true
        this.action = 'costo'
        this.handleTitle = "Costeo de presupuesto"
        this.id = index
      },
      onFiltered (filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length
        this.currentPage = 1
      }
    },
  }
</script>
