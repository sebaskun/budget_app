<template>
  <b-form-input
    :type="type"
    ref="inputValue"
    :value="getValue"
    @input="updateValue">
  </b-form-input>
</template>

<script>
export default {
  props:['value', 'type', 'format'],
  computed: {
    getValue(){
      let value = this.value
      if (this.type=="number"){
        const p = /%/
        if (p.test(this.format)){
          value = value * 100
        }
      }
      console.log("value:", value)
      return value
    }
  },
  methods:{
    updateValue(e){
      let value = e
      if (this.type=="number"){
        const p = /%/
        if (p.test(this.format)){
          value = value * 0.01
        }
      }
      this.$emit('input', value)
    }
  }
}
</script>
