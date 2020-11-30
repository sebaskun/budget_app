<template>
  <tr>
      <th>{{equipment.get_resource_label}}</th>
      <td class="text-right">
        <template v-if="!editing">
          {{equipment.quantity|decimal}}
        </template>
        <template v-else>
          <b-form-input
            id='quantity'
            type="number"
            step="0.01"
            v-model="equipment.quantity">
          </b-form-input>
        </template>
      </td>
      <td class="text-right">
        <template v-if="!editing">
          {{equipment.time_valorize|decimal}} mes
        </template>
        <template v-else>
          <b-form-input
            id='time_valorize'
            type="number"
            step="0.01"
            v-model="equipment.time_valorize">
          </b-form-input>
        </template>
      </td>
      <td class="text-right">
        <template v-if="!editing">
          {{equipment.hours_equipment_operation|decimal}}
        </template>
        <template v-else>
          <b-form-input
            id='hours_equipment_operation'
            type="number"
            step="0.01"
            v-model="equipment.hours_equipment_operation">
          </b-form-input>
        </template>
      </td>
      <td class="text-right">{{equipment.get_standby_estimated_hours|decimal}} Horas</td>
      <td class="text-right">{{equipment.get_standby_hours|decimal}}</td>
      <td class="text-right">{{standBy|decimal}}</td>
      <td class="text-right">{{equipment.get_cost_unit|currency(budget.currency)}}</td>
      <td class="text-right">{{equipment.get_standby_cost|currency(budget.currency)}}</td>
      <td class="text-right">
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
      </td>
  </tr>
</template>

<script>

  var numeral = require('numeral')
  export default {
    props:['equipment', 'budget', 'index'],
    data() {
      return {
        editing: false,
        quantity: 0,
        time_valorize: 0,
        hours_equipment_operation: 0
      }
    },
    computed:{
      standBy(){
        return this.equipment.get_standby_estimated_hours - this.equipment.get_standby_hours
      },
    },
    methods: {
      remove(){
        console.log("remover item")
      },
      edit(){
        this.quantity = this.equipment.quantity
        this.time_valorize = this.equipment.time_valorize
        this.hours_equipment_operation = this.equipment.hours_equipment_operation
        this.editing = true
        console.log(`edit item ${this.equipment.name}`)
      },
      save(){
        this.editing = false
        let obj = {
          quantity: this.equipment.quantity,
          time_valorize: this.equipment.time_valorize,
          hours_equipment_operation: this.equipment.hours_equipment_operation
        }
        let url = `/budget/api/equipment_budget/${this.equipment.pk}/`
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
        this.equipment.quantity = this.quantity
        this.equipment.time_valorize = this.time_valorize
        this.equipment.hours_equipment_operation = this.hours_equipment_operation
        this.editing = false
        console.log(`edit item ${this.equipment.name}`)
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
