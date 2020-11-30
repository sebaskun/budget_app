<template>
  <li class="list-group-item task-list-item">
      <span class="description">{{item.get_resource_label}}</span>
      <span class="quantity">
        <template v-if="!editing">
          {{item.quantity|decimal}}
        </template>
        <template v-else>
          <b-form-input
            id='quantity'
            type="number"
            step="0.01"
            v-model="item.quantity">
          </b-form-input>
        </template>
      </span>
      <span class="quantity">
        <template v-if="!editing">
          {{item.time_valorize|decimal}} mes
        </template>
        <template v-else>
          <b-form-input
            id='time_valorize'
            type="number"
            step="0.01"
            v-model="item.time_valorize">
          </b-form-input>
        </template>
      </span>
      <span class="quantity">
        <template v-if="!editing">
          {{item.amortization|decimal('0.00%')}}
        </template>
        <template v-else>
          <b-form-input
            id='amortization'
            type="number"
            step="0.01"
            v-model="item.amortization">
          </b-form-input>
        </template>
      </span>
      <span class="quantity">{{item.get_cost_unit|currency(budget.currency)}}</span>
      <span class="quantity">{{item.get_overhead_cost|currency(budget.currency)}}</span>
      <span class="quantity">{{getRatio(item.get_overhead_cost)|decimal('0.00%')}}</span>
      <span class="options">
        <template v-if="!editing">
          <a @click="edit">
              <icon name="pencil"></icon>
          </a>
        </template>
        <template v-else>
          <a @click="save">
              <icon name="check"></icon>
          </a>
          <a @click="cancel">
              <icon name="times"></icon>
          </a>
        </template>
      </span>
  </li>
</template>

<script>

  var numeral = require('numeral')
  export default {
    props:['item', 'index', 'total-overhead', 'budget'],
    data() {
      return {
        editing: false,
        quantity: 0,
        time_valorize: 0
      }
    },
    methods: {
      getRatio(value){
        let total = value / this.totalOverhead
        // console.log("Value, total:", value, total)
        return total
      },
      edit(){
        this.quantity = this.item.quantity
        this.time_valorize = this.item.time_valorize
        this.amortization = this.item.amortization
        this.editing = true
        // console.log(`edit item ${this.item.name}`)
      },
      save(){
        this.editing = false
        let obj = {
          quantity: this.item.quantity,
          time_valorize: this.item.time_valorize,
          amortization: this.item.amortization
        }
        let url = `/budget/api/material_budget/${this.item.pk}/`
        this.$http.patch(url, obj)
          .then((response) => {
            this.$emit('updated')
          })
          .catch((err) => {
            console.log("error en save", err)
          })
      },
      cancel(){
        this.item.quantity = this.quantity
        this.item.time_valorize = this.time_valorize
        this.item.amortization = this.amortization
        this.editing = false
        // console.log(`edit item ${this.item.name}`)
      },
    }
  }
</script>

<style>
  .task-list-item .quantity{
    display: inline-block;
    min-width: 80px;
    max-width: 80px;
  }
</style>
