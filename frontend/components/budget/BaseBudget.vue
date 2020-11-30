<template>
  <b-row>
    <b-col md="10">
      <div class="container-fluid">
        <transition name="fade" mode="out-in">

            <router-view></router-view>

        </transition>
      </div>
      <!-- <b-row class="bd-content">
        <b-col md=12 class="my-1">
          <router-view></router-view>
        </b-col>
      </b-row> -->

    </b-col>
    <b-col md="2">
      <b-tabs content-class="mt-3">
        <b-tab title="Menú" active><app-menu/></b-tab>
        <b-tab title="Configuración"><app-config/></b-tab>
      </b-tabs>
    </b-col>
  </b-row>
</template>

<script>

  import Menu from "./nav/Menu.vue"
  import Config from "./Configuracion.vue"

  export default {
      components: {
          'app-menu': Menu,
          'app-config': Config,
      },
      created() {
        this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
      },
      computed: {
        budget(){
          return this.$store.getters['budget/getSelectedBudget']
        },
      },
  }
</script>
