<template>
  <li class="list-group-item task-list-item ">
    <template v-if="!editing">
      <span class="description">{{resource.get_resource_label}}</span>
      <span class="price">{{resource.get_resource_price|currency(budget.currency)}}</span>
      <span class="efficiency">{{resource.get_efficiency|decimal}}</span>
      <span class="quantity">{{resource.quantity|decimal}}</span>
      <span class="subtotal">{{resource.get_subtotal|currency(budget.currency)}}</span>
      <span class="options">
        <a @click="remove">
            <icon name="trash"></icon>
        </a>
      </span>
    </template>
  </li>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    props: ["resource"],
    data(){
      return{
        editing: false
      }
    },
    computed: {
      ...mapGetters({
          budget: 'getSelectedBudget',
          task: 'getSelectedTask'
      }),
    },
    methods: {
      edit(){

      },
      remove(){
        // console.log("Remove resource::", this.resource)
        this.$emit("remove", this.resource)
      },
      // subtotal(){
      //   this.resource.get_price_manpower * this.resource.efficiency * this.resource.quantity
      // }
    }
  }
</script>

<style>
    .task-list-item {
        display: flex;
        justify-content: space-between;
    }
    .task-list-item a {
        text-decoration: none;
    }
    .task-list-item.editing {
        box-shadow: inset 0 0 5px #999;
    }
    .task-list-item input,
    .task-list-item .description,
    .task-list-item .price,
    .task-list-item .efficiency,
    .task-list-item .quantity,
    .task-list-item .subtotal,
    .task-list-item .options,
    {
        flex: 1;
        padding: 0 5px;
    }
    .task-list-item .description{
      display: inline-block;
      /* min-width: 450px; */
      min-width: 33%;
    }
    .task-list-item .price{
      display: inline-block;
      min-width: 90px;
      text-align: right;
    }
    .task-list-item .efficiency{
      display: inline-block;
      min-width: 90px;
      text-align: right;
    }
    .task-list-item .quantity{
      display: inline-block;
      min-width: 90px;
      text-align: right;
    }
    .task-list-item .subtotal{
      display: inline-block;
      min-width: 90px;
      text-align: right;
    }
    .task-list-item .options{
      display: inline-block;
      min-width: 20px;
      padding-left: 15px;
    }



    .task-list-item input {
        border: 0;
    }
    .task-list-item input:focus {
        outline: none;
    }
    .task-list-item.completed .description .price .efficiency .quantity{
        text-decoration: line-through;
    }
    .task-list-item.completed, .task-list-item.completed a {
        color: #999;
    }
</style>
