<template>
  <tr>
      <th>{{ values.label }}</th>
      <td class="text-right" v-for="(item, index) in values.fields" :key="index">
        <template v-if="item.editable">
          <template v-if="!editingForm">
            {{values.items[item.key]|decimal(item.format)}}
          </template>
          <template v-else>
            <b-form-input
              id='scheduled_completion'
              type="number"
              min="0"
              step="1"
              v-model="values.items[item.key]">
            </b-form-input>
          </template>
        </template>
        <template v-else>
          <template v-if="!item.isFalse">
            {{values.items[item.key]}}
          </template>
        </template>
      </td>
      <td class="text-right" v-if="showRatioCalculed">
        {{getRatioItem|decimal("0.0000%")}}
      </td>
      <td class="text-right">
        {{getTotalItem|decimal("0,000.00")}}
      </td>
      <td class="text-right">
        <template v-if="!editingForm">
          <a @click="editItem()">
              <icon name="pencil"></icon>
          </a>
        </template>
        <template v-else>
          <a @click="saveItem()">
              <icon name="check"></icon>
          </a>
          <a @click="cancelItem()">
              <icon name="times"></icon>
          </a>
        </template>
      </td>
  </tr>

</template>

<script>

  export default {
      props:{
        values: {
          required: true,
          type: Object,
        },
        showRatioCalculed: {
          required: false,
          default: true
        },
        precioVentaSinImpuesto: {
          required: true,
          default: 0
        }
      },
      data() {
        return {
          editingForm: false,
          // total: 1,
          backDataForm: {
            ratio_guarantee_faithful_compliance: "",
            get_period_faithful_compliance: "",
            ratio2_guarantee_faithful_compliance: ""
          }
        }
      },

      computed:{
        getRatioItem(){
          let total = 1
          for (const item in this.values.items){
            total = total * this.values.items[item]
          }
          return total
        },
        getTotalItem(){
          return this.precioVentaSinImpuesto * this.getRatioItem
        }
      },
      watch:{
        getRatioItem(val){
          this.$emit('ratioCalculed', val)
        }
      },
      methods: {
        cancelItem(){
          this.values.scheduled_completion = this.backDataForm.scheduled_completion
          this.editingForm = false
        },
        saveItem(){
          this.$emit("onSave", this.values.items)
          this.editingForm = false
        },
        editItem(){
          this.backDataForm.scheduled_completion = this.values.scheduled_completion
          this.editingForm = true
        },
      },
  }
</script>
