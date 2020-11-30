<template>
  <b-row class="bd-title">
    <b-col md="12" class="my-1 truncate-ellipsis">
      <h5>{{title}}</h5>
    </b-col>
    <b-col md="12" class="my-1">
      <div class="head-subtitle"><h6>{{subTitle}}</h6></div>
      <div class="head-subtitle"><slot name="subTitle"></slot></div>
      <div class="head-options"><slot name="options"></slot></div>
    </b-col>
  </b-row>

</template>

<script>
export default {
  name: 'AppTitle',
  props:['title', 'subTitle']
}
</script>
