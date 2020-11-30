<template>
  <div>
    <b-navbar toggleable="md" type="dark" class="navbar-inverse sticky-top">

      <b-navbar-toggle target="nav_collapse">Proyecta</b-navbar-toggle>

      <b-navbar-brand to="/"><img class="logo-brand" src="../assets/inmac-logo-blanco.svg" alt="">Proyecta</b-navbar-brand>

      <b-navbar-nav>
          <b-nav-item :to="{ name: 'home' }">Inicio</b-nav-item>
          <b-nav-item :to="{ name: 'budget' }">Presupuestos</b-nav-item>
          <b-nav-item-dropdown right>
            <!-- Using button-content slot -->
            <template slot="button-content">
              Recursos
            </template>
            <b-dropdown-item :to="{ name: 'resource-manpower' }">Mano de obra</b-dropdown-item>
            <b-dropdown-item :to="{ name: 'resource-material' }">Materiales</b-dropdown-item>
            <b-dropdown-item :to="{ name: 'resource-subcontract' }">Subcontratos</b-dropdown-item>
            <b-dropdown-item :to="{ name: 'resource-equipment' }">Equipos</b-dropdown-item>
            <b-dropdown-item :to="{ name: 'resource-vacuna'}">Vacunas</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown right>
            <!-- Using button-content slot -->
            <template slot="button-content">
              Administrador
            </template>
            <b-dropdown-item :to="{ name: 'admin-grupo' }">Grupos</b-dropdown-item>
            <b-dropdown-item :to="{ name: 'admin-regimen' }">Regímenes</b-dropdown-item>
            <b-dropdown-item :to="{ name: 'admin-certificado' }">Certificados</b-dropdown-item>
            <b-dropdown-item :to="{ name: 'client' }">Clientes</b-dropdown-item>
          </b-nav-item-dropdown>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right>
          <!-- Using button-content slot -->
          <template slot="button-content">
            Usuario
          </template>
          <b-dropdown-item href="#" disabled>Profile</b-dropdown-item>
          <b-dropdown-item href="/accounts/logout">Salir</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>

    </b-navbar>
    <div class="container-fluid">
      <transition name="fade" mode="out-in">
        <!-- <keep-alive> -->
        <router-view></router-view>
        <!-- </keep-alive> -->
      </transition>
    </div>


  </div>
</template>

<script>
export default {
  // mounted() {
  //   this.$store.dispatch('getBudgetList')
  //   this.$store.dispatch('requestClientList')
  // }
}
</script>
