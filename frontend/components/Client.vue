<template>
    <div>
        <div v-if="!isEditing">
          <b-card :title=title>
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
                  <b-button @click="onAddItem()" variant="primary" class="float-right">Crear un cliente</b-button>
              </b-col>
            </b-row>

            <b-table
              striped hover :items="items" :fields="fields"
              :filter="filter" @filtered="onFiltered">
              <template slot="actions" slot-scope="row">
                  <b-button size="sm" @click.stop="onEditItem(row.item.id)" class="mr-1">Editar</b-button>
                  <b-button size="sm" @click.stop="row.toggleDetails">
                      {{ row.detailsShowing ? 'Ocultar' : 'Mostrar' }} Detalle </b-button>
              </template>
              <template slot="image" slot-scope="row"><img :src="row.item.get_image_miniature_50_0" alt=""></template>
              <template slot="row-details" slot-scope="row">
                  <b-card>
                      <p>{{row.item.description}}</p>

                  </b-card>
              </template>
            </b-table>
          </b-card>
        </div>
        <div v-else>
            <transition name="fade" mode="out-in" appear>
                <b-card :title=handleTitle style="max-width: 40rem;">
                    <app-handle-item :action="action" :id="id" @itemAdded="getItems" @canceled="isEditing=false"></app-handle-item>
                </b-card>
            </transition>
        </div>
    </div>
</template>

<script>

import HandleItem from "./client/HandleClient.vue"
const url_api = '/client/api/clients/'

export default {
    components: {
        'app-handle-item': HandleItem,
    },
    data() { 
        return {
            searchQuery: '',
            title: "Cliente",
            handleTitle: "",
            filtered_items: [],
            items: [],
            fields: [
                {key:'image', label: 'Logo'}, 
                {key:'name', label: 'Nombre', sortable: true},
                {key:'initials', label: 'Iniciales', sortable: true},
                {key:'actions', label: 'Acciones'}],
            isEditing: false,
            action: "add",
            filter: null,
            id: ""
        }
    },
    mounted: function() {
      this.getItems()
    },
    methods: {
      onAddItem() {
        this.isEditing = true
        this.action = "add"
        this.handleTitle = "Crear Cliente"
      },
      onEditItem(index) {
        this.isEditing = true
        this.action = 'edit'
        this.handleTitle = "Modificar Cliente"
        this.id = index
      },
      getItems() {
        this.action = 'add'
        let url = url_api
        this.$http.get(url)
            .then((response) => {
                this.items = response.data.results
                this.filtered_items = this.items
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
    }
  }
</script>
