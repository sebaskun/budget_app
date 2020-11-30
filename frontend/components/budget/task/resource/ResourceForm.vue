<template>
  <div>
    <b-form>
      <b-row>
        <b-col lg="6">
          <b-form-group id='resource_group'>
            <v-select id="resource"
                      @input="onChangeValue"
                      v-model="selectedResource"
                      :options="resources"
                      label="get_resource_label">
              <template slot="option" slot-scope="option">
                <div>
                  {{ `${option.get_resource_code} ${option.get_resource_name} (${option.unit})` }}
                </div>
              </template>
            </v-select>
          </b-form-group>
        </b-col>
        <b-col lg="2">
          <b-form-group id="quantity_group">
            <b-form-input
              id="quantity"
              type="number"
              step=".01"
              v-model="form.quantity"
              placeholder="Cantidad">
            </b-form-input>
          </b-form-group>
        </b-col>
        <b-col lg="2" v-if="showEfficiency">
          <b-form-group id="efficiency_group">
            <b-form-input
              id="efficiency"
              type="number"
              step=".01"
              v-model="form.efficiency"
              placeholder="Rendimiento">
            </b-form-input>
          </b-form-group>
        </b-col>
        <b-col lg="2">
          <b-button type="submit" @click.prevent="onSubmit" variant="primary">Agregar</b-button>
        </b-col>
      </b-row>
    </b-form>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    props: {
      // task: {type: Object, required: true},
      typeResource: {
        validator: function (value) {
        // The value must match one of these strings
          return ['material', 'subcontract', 'manpower', 'equipment'].indexOf(value) !== -1
        }
      }
    },
    data(){
      return{
        selectedResource: "",
        budgetId: null,
        // resources: [],
        form: {
            task: null,
            // resource: null,
            quantity: null,
            efficiency: null,
        },
        showEfficiency: false
      }
    },
    watch: {
      budget(value, oldValue){
        const typeResource = this.typeResource.capitalize()
        this.$store.dispatch(`budget/requestBudget${typeResource}s`, value.id)
        // this.resources = this.$store.dispatch(`requestBudget${typeResource}s`, value.id)
      },
    },
    computed: {
      ...mapGetters({
          budget: 'budget/getSelectedBudget',
          task: 'getSelectedTask'
      }),
      resources(){
        const typeResource = this.typeResource.capitalize()
        // return this.$store.state.todos.filter(todo => todo.done).length
        // return this.$store.state[`availableBudget${typeResource}s`]
        return this.$store.getters[`budget/getAvailableBudget${typeResource}s`]
      }
    },
    mounted() {
      // const typeResource = this.typeResource.capitalize()
      // console.log("___typeResource__", typeResource)
      // this.$store.dispatch(`requestBudget${typeResource}s`, this.budget.id)
      if (['material', 'subcontract'].includes(this.typeResource)){
      //   console.log("Task Efficiency:::::", this.efficiency)
      //   // this.form.efficiency = (8 / this.efficiency)
      // }else{
        this.showEfficiency = true
      }
    },
    methods: {
      getResourcesBudget() {
        let url = `/budget/api/budgets/${this.budget.id}/${this.typeResource}s/`
        // console.log("url:::", url)
        this.$http.get(url)
          .then((response) => {
            this.resources = response.data
          })
          .catch((err) => {
            console.log(err);
          })
      },
      onChangeValue(e) {
        if (Boolean(e)){
          this.$set(this.form, this.typeResource, e[this.typeResource])
          this.$set(this.form, this.typeResource + '_budget', e['id'])
        }
      },
      onSubmit (evt) {
        evt.preventDefault()
        this.form.task = this.task.id
        // if (this.typeResource!='material'){
        //   // console.log("Task Efficiency:::::", this.efficiency)
        //   this.form.efficiency = parseFloat(8 / this.task.efficiency).toFixed(2)
        // }
        this.$emit("onEdit", this.form)
      }
    }
  }
</script>
