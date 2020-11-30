<template>
  <tr>
      <th>{{ values.label }}</th>
      <td class="text-right" v-for="(item, index) in values.fields" :key="index">
        <template v-if="item.editable">
          <template v-if="!editingForm">
            {{values.items[item.key]|decimal(item.format)}}
          </template>
          <template v-else>
            <app-custom-input
              type="number"
              min="0"
              :format="item.format"
              v-model="values.items[item.key]"/>
          </template>
        </template>
        <template v-else>
          <template v-if="!item.isFalse">
            {{values.items[item.key]}}
          </template>
        </template>
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
  import CustomInput from "../../utils/CustomInput.vue"
  export default {
      components: {
        'app-custom-input': CustomInput
      },
      props:{
        values: {
          required: true,
          type: Object,
        },
      },
      data() {
        return {
          editingForm: false,
          // total: 1,
          backItems: this.values.items,
        }
      },
      // watch:{
      //   values(val){
      //     console.log("values", val)
      //   }
      // },
      methods: {
        cancelItem(){
          console.log("Items:", this.backItems)
          this.values.items = this.backItems
          this.editingForm = false
        },
        saveItem(){
          this.$emit("onSave", this.values.items)
          this.editingForm = false
        },
        editItem(){
          this.editingForm = true
        },
      },
  }
</script>
