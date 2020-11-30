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
      <span class="quantity">{{manpower.get_business_cost|currency(budget.currency)}}</span>
      <span class="quantity">{{manpower.get_overhead_cost|currency(budget.currency)}}</span>
      <span class="quantity">{{getRatio(manpower.get_overhead_cost)|decimal('0.00%')}}</span>
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
    props:['manpower', 'totalOverhead', 'budget'],
    data() {
      return {
        editing: false,
        quantity: 0,
        time_valorize: 0
      }
    },
    // computed:{
    //   estimatedHours(){
    //     let value = this.manpower.quantity * this.manpower.time_valorize * 30 * 8
    //     this.$set(this.manpower, 'estimated_hour', value)
    //     return value
    //   },
    //   standBy(){
    //     let value = this.manpower.estimated_hour - this.manpower.hour_apu
    //     this.$set(this.manpower, "stand_by", value)
    //     return value
    //   },
    //   costStandBy(){
    //     let value = 0
    //     value = this.manpower.stand_by * this.manpower.price
    //     if (value>0){
    //       this.$set(this.manpower, "cost_stand_by", value)
    //       return value
    //     }
    //     this.$set(this.manpower, "cost_stand_by", 0)
    //     return 0
    //   },
    //   water(){
    //     let value = (3.5/20) * this.manpower.quantity * this.manpower.time_valorize * 30
    //     this.$set(this.manpower, "water", value)
    //     return value
    //   },
    //   subtotal(){
    //     let value = this.manpower.quantity * this.manpower.time_valorize * this.manpower.business_cost
    //     this.$set(this.manpower, "subtotal", value)
    //     return value
    //   }
    // },
    methods: {
      getRatio(value){
        return value / this.totalOverhead
      },
      remove(){
        console.log("remover item")
      },
      edit(){
        this.quantity = this.manpower.quantity
        this.time_valorize = this.manpower.time_valorize
        this.editing = true
        // console.log(`edit item ${this.manpower.name}`)
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
