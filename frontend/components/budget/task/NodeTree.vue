<template>
  <li :class="{parent: isFolder}">
    <div class="container-row">
      <div class="row" :class="{'row-parent': isFolder}">
        <div class="col col-400">
          <span @click="toggle" v-if="isFolder" class="nested-button">
            <icon v-if="open" name="minus-square"></icon>
            <icon v-else name="plus-square"></icon>
          </span>
          <template v-if="!isFolder">
            <router-link :to="{ name:'budget-apu', params: {budget: node.budget, task: node.id} }">{{ (node.wbs ? node.wbs +"-": "") +node.name }}</router-link>
          </template>
          <template v-else>
            <span>{{ (node.wbs ? node.wbs + "-": "") +node.name }}</span>
          </template>
        </div>
        <div class="col-sm col-50">
          {{ node.unit }}
        </div>
        <div class="col-sm text-right col-100">
          <template v-if="!isFolder">
            {{ node.quantity }}
          </template>
        </div>
        <div class="col-sm text-right col-100">
          <template v-if="!isFolder">
            {{ node.get_unit_subtotal|currency(budget.currency) }}
          </template>
        </div>
        <div class="col-sm text-right col-100"  :class="{total: isFolder, subtotal: !isFolder}">
          {{ node.get_subtotal|currency(budget.currency) }}
        </div>
        <template v-if="edit">
          <div class="col-sm col-100">
            <b-button-toolbar>
              <b-button-group size="sm">
                <b-btn @click="createNode()">+</b-btn>
                <b-btn @click="deleteNode()">-</b-btn>
                <b-btn @click="removePositionNode()">^</b-btn>
                <b-btn @click="addPositionNode()">v</b-btn>
                <b-btn @click="removeLevelNode()"><-</b-btn>
                <b-btn @click="addLevelNode()">-></b-btn>
              </b-button-group>
            </b-button-toolbar>
          </div>
        </template>
      </div>
    </div>
    <ul v-show="open" v-if="isFolder">
      <node
        v-for="(child, index) in node.children"
        :node="child"
        :key="index">
      </node>
    </ul>
  </li>
</template>

<script>
  // var numeral = require('numeral')
  import { mapGetters } from 'vuex'

  export default {
    name: "node",
    props: ['node'],
    data() {
      return {
        open: true,
        hasChildren: false
      }
    },
    computed: {
      ...mapGetters({
          budget: 'getSelectedBudget',
          edit: 'getEditingTree',
      }),
      isFolder () {
        // console.log(">>>>hijos>>>>>", this.node.get_children)
        const isFolder = this.node.children && this.node.children.length
        if(isFolder){
          this.hasChildren = true
          let total = 0
          this.node.children.forEach(valor => total += valor.get_subtotal)
          this.node.get_subtotal = total
        }
        return isFolder
      },
      // subtotal() {
      //   // let subTotal = 0
      //   if(this.isFolder) console.log("-----Es padre---", this.node.get_children)
      //   return this.node.price * this.node.quantity
      // }
    },
    methods: {
      toggle () {
        if (this.isFolder) {
          this.open = !this.open
        }
      },
      get_total () {
        let sum = 0
        this.node.children.forEach(function(valor, indice, array){
          sum += valor.get_subtotal
        })
        return sum
      },
      alterNode(data) {
        data.taskid = this.node.id
        data.budgetid = this.budget.id
        let obj=this
        this.$http.post('budget/api/nodeapi', data).then((response) => {
          // obj.$emit('update')
          this.$store.dispatch('getTaskListByBudget', this.budget.id)
          console.log(response)
        }, (err) => {console.log(err)})
      },
      createNode () {
        let data={method: 'insert'}
        this.alterNode(data)
      },
      deleteNode(){
        let data={method: 'delete' }
        this.alterNode(data)
      },
      addLevelNode(){
        let data={method: '+level'}
        this.alterNode(data)
      },
      removeLevelNode(){
        let data={method: '-level'}
        this.alterNode(data)
      },
      addPositionNode(){
        let data={method: '+position'}
        this.alterNode(data)
      },
      removePositionNode(){
        let data={method: '-position'}
        this.alterNode(data)
      },
    },
  }
</script>
