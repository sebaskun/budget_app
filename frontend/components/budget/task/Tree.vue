<template>
  <div class="tree">

    <div class="container-row">
      <div class="row">
        <div class="col col-400">
          Descripción
        </div>
        <div class="col-sm col-50">
          Und.
        </div>
        <div class="col-sm text-right col-100">
          Cantidad
        </div>
        <div class="col-sm text-right col-100">
          P.U.
        </div>
        <div class="col-sm col-100">
          Subtotal
        </div>

        <div class="col-sm col-100" v-show="edit">
          Opciones
        </div>

      </div>
    </div>


    <ul class="tree-list">
      <node-tree :node="tasks"></node-tree>
    </ul>
  </div>
</template>

<script>
  import NodeTree from "./NodeTree.vue"
  import { mapGetters } from 'vuex'

  export default {
    components: {
      NodeTree
    },
    props: [
      "treeData",
    ],
    computed: {
      ...mapGetters({
          edit: 'getEditingTree',
          tasks: 'getAvailableTasks'
      }),
    },
    // methods: {
    //   updateTasks(){
    //     console.log("actualizar tareas....")
    //   }
    // }
  }
</script>

<style>
  .tree-list{
    padding-left: 0em;
  }
</style>
