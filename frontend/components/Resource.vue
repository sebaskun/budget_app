<template>
    <div>
        <div v-if="!isEditing">
          <b-card :title=title
              tag="article">
            <b-row>
              <b-col md="6" class="my-1">
                <b-form-group horizontal label="Filtro" class="mb-0">
                  <b-input-group>
                    <b-form-input v-model="filter" placeholder="Escriba para buscar" />
                    <b-input-group-append>
                      <b-btn :disabled="!filter" @click="filter = ''">Limpiar</b-btn>
                    </b-input-group-append>
                  </b-input-group>
                </b-form-group>
              </b-col>
              <b-col md="6" class="my-1">
                  <b-button @click="onAddItem()" variant="primary" class="float-right">Crear un recurso equipo</b-button>
              </b-col>
            </b-row>

            <b-pagination size="md" :total-rows="totalRows" v-model="currentPage" :per-page="100"></b-pagination>
            <b-table
              striped hover :items="items" :fields="fields">
              <template slot="actions" slot-scope="row">
                  <b-button size="sm" @click.stop="onEditItem(row.item.id)" class="mr-1">Editar</b-button>
                  <b-button size="sm" @click.stop="row.toggleDetails">
                      {{ row.detailsShowing ? 'Ocultar' : 'Mostrar' }} Detalle </b-button>
              </template>
              <template slot="row-details" slot-scope="row">
                  <b-card>
                      <p>{{row.item.description}}</p>

                  </b-card>
              </template>
            </b-table>
            <b-pagination size="md" :total-rows="totalRows" v-model="currentPage" :per-page="100"></b-pagination>
          </b-card>
        </div>
        <div v-else>
            <transition name="fade" mode="out-in" appear>
                <b-card :title=handleTitle style="max-width: 40rem;">
                    <app-handle-item :action="action" :id="id" @itemAdded="getItems(currentPage)" @canceled="isEditing=false"></app-handle-item>
                </b-card>
            </transition>
        </div>
    </div>
</template>

<script>

import HandleItem from "./resource/HandleEquipment.vue"
const url_api = '/resource/api/equipment/'

export default {
    components: {
        'app-handle-item': HandleItem,
    },
    data() {
        return {
            totalRows:0,
            currentPage:1,
            searchQuery: '',
            title: "Recurso de Equipo",
            handleTitle: "",
            filtered_items: [],
            items: [],
            fields: [
                {key:'code', label: 'Código', sortable: true},
                {key:'name', label: 'Nombre', sortable: true},
                {key:'unit', label: 'Unidad', sortable: false},
                {key:'currency', label: 'Moneda', sortable: false},
                {key:'cost', label: 'Costo', sortable: false},
                {key:'hours_equipment_operation', label: 'H.Operac.', sortable: false},
                {key:'actions', label: 'Acciones'}],
            isEditing: false,
            action: "add",
            filter: '',
            id: ""
        }
    },
    mounted: function() {
      this.getItems(1)
    },
    methods: {
      onAddItem() {
        this.isEditing = true
        this.action = "add"
        this.handleTitle = "Crear Recurso Equipo"
      },
      onEditItem(index) {
        this.isEditing = true
        this.action = 'edit'
        this.handleTitle = "Modificar Recurso Equipo"
        this.id = index
      },
      getItems(pag) {
        this.action = 'add'
        let url = url_api+`?search=${this.filter}&page=${pag}`
        this.$http.get(url)
            .then((response) => {
                this.items = response.data.results
                this.filtered_items = this.items
                this.totalRows = response.data.count
                this.isEditing = false
            })
            .catch((err) => {
                console.log(err)
            })
      },
      onFiltered (filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length
        this.currentPage = 1
      }
    },
    watch: {
        filter: function (to, from) {
            if (this.currentPage != 1){
                this.currentPage = 1
            } else {
                this.getItems(1)
            }
        },
        currentPage: function (to, from) {
            this.getItems(to)
        }
    }
  }
</script>
