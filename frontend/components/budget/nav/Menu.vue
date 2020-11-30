<template>
  <b-row>
    <div class="bd-content">

      <h6>Vistas</h6>
      <b-nav vertical class="sidebar-section">
        <b-nav-item :to="{name: 'budget-partidas', params:{budget: budgetId, }}">Partidas</b-nav-item>
        <b-nav-item :to="{name: 'budget-overhead', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">Gastos Generales</b-nav-item>
        <b-nav-item :to="{name: 'budget-standby', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">Stand by</b-nav-item>
        <b-nav-item :to="{name: 'budget-close', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">Hoja de cierre</b-nav-item>
        <b-nav-item :to="{name: 'budget-estructura-costos', params:{budget: budgetId, }}">Estructura de costos</b-nav-item>
      </b-nav>
      <br>
      <h6>Recursos</h6>
      <b-nav vertical class="sidebar-section">
        <b-nav-item :to="{name: 'budget-material', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">Material</b-nav-item>
        <b-nav-item :to="{name: 'budget-subcontract', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">Subcontrato</b-nav-item>
        <b-nav-item :to="{name: 'budget-equipment', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">Equipo</b-nav-item>
        <b-nav-item :to="{name: 'budget-manpower', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">Mano de obra</b-nav-item>
        <b-nav-item :to="{name: 'budget-certificacion', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">Certificacion</b-nav-item>
        <b-nav-item :to="{name: 'budget-epp', params: {budget: $route.params.budget}, query: {task: $route.params.task}}">EPP</b-nav-item>
      </b-nav>
      <br>
    </div>
  </b-row>
</template>

<script>
export default {
    data() {
      return {
        taskId: this.$route.params.task,
        budgetId: this.$route.params.budget
      }
    },
    watch:{
      '$route'(to, from){
        this.taskId = this.$route.params.task
        this.budgetId = this.$route.params.budget
      },
    },
  }
</script>
