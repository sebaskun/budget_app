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
                  <b-button @click="onAddItem()" variant="primary" class="float-right">Crear un recurso mano de obra</b-button>
              </b-col>
            </b-row>

            <b-pagination size="md" :total-rows="totalRows" v-model="currentPage" :per-page="100"></b-pagination>
            <b-table
              striped hover :items="items" :fields="fields">
              <template slot="actions" slot-scope="row">
                  <b-button size="sm" @click.stop="onEditItem(row.item.id)" class="mr-1">Editar</b-button>
                  <b-button size="sm" @click.stop="onDeleteItem(row.item)" class="mr-1">Eliminar</b-button>
              </template>
              <template slot="business_cost" slot-scope="row">
                  {{ row.value|currency(row.item.currency) }}
              </template>
            </b-table>
            <b-pagination size="md" :total-rows="totalRows" v-model="currentPage" :per-page="100"></b-pagination>
          </b-card>
        </div>
        <div v-else>
            <transition name="fade" mode="out-in" appear>
                <b-card :title=title style="max-width: 40rem;">
                    <app-handle-item :action="action" :id="id" @itemAdded="getItems(1)" @canceled="isEditing=false"></app-handle-item>
                </b-card>
            </transition>
        </div>
    </div>
</template>

<script>

import HandleItem from "./resource/HandleManpower.vue"
const url_api = '/resource/api/manpower/'

export default {
    components: {
        'app-handle-item': HandleItem,
    },
    data() {
        return {
            totalRows:0,
            currentPage:1,
            searchQuery: '',
            title: "Recurso de Mano de Obra",
            filtered_items: [],
            items: [],
            fields: [
                {key:'code', label: 'Código', sortable: true},
                {key:'name', label: 'Nombre', sortable: true},
                {key:'unit', label: 'Unidad', sortable: true},
                {key:'sueldo_bruto', label: 'Sueldo Bruto', sortable: true},
                {key:'type_cost', label: 'Tipo Costo', sortable: true},
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
      },
      onEditItem(index) {
        this.isEditing = true
        this.action = 'edit'
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
                console.log(response)
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
      },
      onDeleteItem(index) {
        const url = `/resource/api/manpower/${index.id}`
        this.$swal({
          title: `¿Está seguro de eliminar el recurso ${index.name}?`,
          text: "Una vez eliminado no se podrá recuperar!",
          type: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Sí, eliminar!'
        })
        .then((willDelete) => {
          if (willDelete.value) {
            this.$http.delete(url)
              .then((response)=>{
                this.$swal({
                  position: 'top-end',
                  toast: true,
                  type: 'success',
                  title: 'Se eliminó correctamente.',
                  showConfirmButton: false,
                  timer: 1500
                })
                this.getItems(this.currentPage)
              })
              .catch((err)=> {
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
