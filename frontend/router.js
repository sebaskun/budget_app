import Vue from 'vue'
import VueRouter from 'vue-router'
import Budget from './components/Budget.vue'
import BaseBudget from './components/budget/BaseBudget.vue'
import PartidasBudget from './components/budget/PartidasBudget.vue'
import EstructuraCostosBudget from './components/budget/EstructuraCostosBudget.vue'
import Overhead from './components/budget/Overhead.vue'
import StandBy from './components/budget/StandBy.vue'
import Close from './components/budget/Close.vue'
import ApuBudget from './components/budget/ApuBudget.vue'
import ResourceManpower from './components/ResourceManpower.vue'
import ResourceMaterial from './components/ResourceMaterial.vue'
import ResourceSubcontract from './components/ResourceSubcontract.vue'
import SettingOverHead from './components/SettingOverHead.vue'
import ResourceEquipment from './components/ResourceEquipment.vue'
import Client from './components/Client.vue'
import ResourceBudget from './components/budget/ResourceBudget.vue'
import AdminGrupo from './components/admin/Grupo.vue'
import AdminRegimen from './components/admin/Regimen.vue'
import AdminCertificado from './components/admin/Certificado.vue'
import CertificacionBudget from './components/budget/CertificacionBudget.vue'
import EPPBudget from './components/budget/EPPBudget.vue'
import ManpowerBudget from './components/budget/ManpowerBudget.vue'
import MaterialBudget from './components/budget/MaterialBudget.vue'
import EquipmentBudget from './components/budget/EquipmentBudget.vue'
import SubcontractBudget from './components/budget/SubcontractBudget.vue'
import ResourceVacuna from './components/ResourceVacuna.vue'

Vue.use(VueRouter)

export default new VueRouter({
    routes: [
        { path: '/', name: 'home', redirect: '/budget',  },
        { path: '/budget', name: 'budget', component: Budget },
        // { path: '/budget/:budget/costing', name: 'budget-costing', component: CostingBudget },
        // { path: '/budget/:budget/overhead', name: 'budget-overhead', component: Overhead },
        // { path: '/budget/:budget/standby', name: 'budget-standby', component: StandBy },
        // { path: '/budget/:budget/close', name: 'budget-close', component: Close },
        // { path: '/budget/:budget/resource/manpower', name: 'budget-manpower', component: ManpowerBudget },
        // { path: '/budget/:budget/resource/:typeResource', name: 'budget-resource', component: ResourceBudget },
        // { path: '/budget/:budget/apu/:task', name: 'budget-apu', component: ApuBudget },
        { path: '/budget/:budget', name: 'budget-base', component: BaseBudget,
            children: [
                { path: '/budget/:budget', name: 'budget-partidas', component: PartidasBudget },
                { path: 'estructura', name: 'budget-estructura-costos', component: EstructuraCostosBudget },
                { path: 'overhead', name: 'budget-overhead', component: Overhead },
                { path: 'standby', name: 'budget-standby', component: StandBy },
                { path: 'close', name: 'budget-close', component: Close },
                { path: 'manpower', name: 'budget-manpower', component: ManpowerBudget },
                { path: 'material', name: 'budget-material', component: MaterialBudget },
                { path: 'subcontract', name: 'budget-subcontract', component: SubcontractBudget },
                { path: 'equipment', name: 'budget-equipment', component: EquipmentBudget },
                { path: 'resource/:typeResource', name: 'budget-resource', component: ResourceBudget },
                { path: 'apu/:task', name: 'budget-apu', component: ApuBudget },
                { path: 'certificacion', name: "budget-certificacion", component: CertificacionBudget },
                { path: 'epp', name: "budget-epp", component: EPPBudget }
            ]
        },
        { path: '/resource/manpower', name: 'resource-manpower', component: ResourceManpower },
        { path: '/resource/material', name: 'resource-material', component: ResourceMaterial },
        { path: '/resource/subcontract', name: 'resource-subcontract', component: ResourceSubcontract },
        { path: '/resource/equipment', name: 'resource-equipment', component: ResourceEquipment },
        { path: '/resource/vacuna', name: 'resource-vacuna', component: ResourceVacuna },
        { path: '/setting/overhead', name: 'setting-overhead', component: SettingOverHead },
        { path: '/client', name: "client", component: Client },
        { path: '/admin/grupo', name: "admin-grupo", component: AdminGrupo },
        { path: '/admin/regimen', name: "admin-regimen", component: AdminRegimen },
        { path: '/admin/certificado', name: "admin-certificado", component: AdminCertificado },
    ],
    // mode: 'history'
})
