<template>
  <li class="list-group-item task-list-item">
      <span class="description">{{manpower.get_resource_label}}</span>
      <span class="quantity">
        <template v-if="!editing">
          {{manpower.quantity|decimal}}
        </template>
        <template v-else>
          <b-form-input
            id='quantity'
            type="number"
            step="0.01"
            v-model="manpower.quantity">
          </b-form-input>
        </template>
      </span>
      <span class="quantity">
        <template v-if="!editing">
          {{manpower.time_valorize|decimal}} mes
        </template>
        <template v-else>
          <b-form-input
            id='time_valorize'
            type="number"
            step="0.01"
            v-model="manpower.time_valorize">
          </b-form-input>
        </template>
      </span>
      <span class="quantity">{{manpower.get_standby_estimated_hours|decimal}} Horas</span>
      <span class="quantity">{{manpower.get_standby_hours|decimal}}</span>
      <span class="quantity">{{standBy|decimal}}</span>
      <span class="quantity">{{manpower.get_cost_unit|currency(budget.currency)}}</span>
      <span class="quantity">{{manpower.get_standby_cost|currency(budget.currency)}}</span>
      <span class="quantity">{{manpower.get_standby_hydration|currency(budget.currency)}}</span>
      <span class="quantity">{{manpower.get_standby_epp|currency(budget.currency)}}</span>
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

  import { mapGetters } from 'vuex'

  export default {
    props:['manpower', 'budget'],
    data() {
      return {
        editing: false,
        quantity: 0,
        time_valorize: 0
      }
    },
    computed:{
      standBy(){
        return this.manpower.get_standby_estimated_hours - this.manpower.get_standby_hours
      },

    },
    methods: {
      remove(){
        console.log("remover item")
      },
      edit(){
        this.quantity = this.manpower.quantity
        this.time_valorize = this.manpower.time_valorize
        this.editing = true
        console.log(`edit item ${this.manpower.name}`)
      },
      save(){
        this.editing = false
        let obj = {
          quantity: this.manpower.quantity,
          time_valorize: this.manpower.time_valorize
        }
        let url = `/budget/api/manpower_budget/${this.manpower.pk}/`
        this.$http.patch(url, obj)
          .then((response) => {
            console.log("Guadado::", response.data)
            this.$emit('updated')
          })
          .catch((err) => {
            console.log("error en save", err)
          })
      },
      cancel(){
        this.editing = false
        console.log(`edit item ${this.manpower.name}`)
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
