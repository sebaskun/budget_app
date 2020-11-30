<template>
  <b-row>
    <b-col md="12">
      <app-title
        :title="budget.code + ' - ' + budget.title"
        subTitle="Hoja de cierre">
        <!-- <template slot="options">
          <app-ratio-budget
            :values="formRatioBudget"
            @onSave="onSaveSubmit"/>
          <app-ratio-mark-up-diff2
            :values="formMarkUpDifferentiated"
            @onSave="onSaveSubmit"/>
        </template> -->
      </app-title>

      <b-row class="bd-content">
        <!-- Costo directo -->
        <b-col md="6" class="my-1">
          <section class="view-data">
            <table class="table table-striped">
              <col width="60">
              <col width="20%">
              <col width="20%">
              <thead>
                <tr>
                  <th class="text-right">DIRECTO:</th>
                  <th class="text-right">{{direct.total|currency(budget.currency)}}</th>
                  <th class="text-right">{{getRatio(1, 1)|decimal('0.00%')}}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>Costo Mano de Obra</th>
                  <td class="text-right">{{ direct.items.manpowers|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(direct.items.manpowers, direct.total)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>Costo Equipos</th>
                  <td class="text-right">{{ direct.items.equipments|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(direct.items.equipments, direct.total)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>Costo Materiales</th>
                  <td class="text-right">{{ direct.items.materials|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(direct.items.materials, direct.total)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>Costo Subcontratos</th>
                  <td class="text-right">{{ direct.items.subcontracts|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(direct.items.subcontracts, direct.total)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>Herramientas menores</th>
                  <td class="text-right">{{ direct.items.min_tools|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(direct.items.min_tools, direct.total)|decimal('0.00%') }}</td>
                </tr>
              </tbody>
            </table>
          </section>
        </b-col>
        <!-- Fin: Costo directo -->
        <!-- Costo indirecto -->
        <b-col md="6" class="my-1">
          <section class="view-data">
            <table class="table table-striped">
              <col width="60%">
              <col width="20%">
              <col width="20%">
              <thead>
                <tr>
                  <th class="text-right">COSTO INDIRECTO:</th>
                  <th class="text-right">{{totalIndirect|currency(budget.currency)}}</th>
                  <th class="text-right">{{getRatio(totalIndirect, direct.total)|decimal('0.00%')}}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>PERSONAL DE DIRECCION TECNICA EN OBRA</th>
                  <td class="text-right">{{ manpowers.total|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(manpowers.total, totalIndirect)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>COSTOS DE STAND BY</th>
                  <td class="text-right">{{ totalStandby|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(totalStandby, totalIndirect)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>TALLER MECÁNICO</th>
                  <td class="text-right">{{ workshops.total|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(workshops.total, totalIndirect)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>TÓPICO - SALUD</th>
                  <td class="text-right">{{ medicals.total|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(medicals.total, totalIndirect)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>GASTO OPERATIVO, OFICINA, CONTINGENCIA</th>
                  <td class="text-right">{{ operatives.total|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(operatives.total, totalIndirect)|decimal('0.00%') }}</td>
                </tr>
                <tr>
                  <th>V A R I O S</th>
                  <td class="text-right">{{ various.total|currency(budget.currency) }}</td>
                  <td class="text-right">{{getRatio(various.total, totalIndirect)|decimal('0.00%') }}</td>
                </tr>
              </tbody>
            </table>


          </section>

        </b-col>
        <!-- Fin: Costo indirecto -->
        <!-- Total costo industrial -->
        <b-col md="12">

            <!-- <rotate-square2></rotate-square2> -->
            <section class="view-data">

            <table class="table table-striped">
              <col width="85%">
              <col width="15%">
              <thead>
                <tr>
                  <th class="text-right">TOTAL COSTO INDUSTRIAL:</th>
                  <th class="text-right">{{totalCostIndustry|currency(budget.currency)}}</th>
                </tr>
              </thead>
            </table>
            </section>
        </b-col>
        <!-- Fin: Total costo industrial -->
        <!-- Plazo de obra -->
        <app-scheduledcompletion
          :scheduledCompletion="formScheduledCompletion"
          @onSaveScheduledCompletion="onSaveSubmit"
        />
        <!-- Fin: Plazo de obra -->

        <b-col md="8" class="my-1">
          <section class="view-data">
            <table class="table table-striped">
              <col width="40%">
              <col width="15%">
              <col width="5%">
              <col width="15%">
              <col width="10%">
              <col width="12%">
              <col width="3%">
              <tbody>

              <app-ratio-mark-up
                :values="frmMarkupGFC"
                :precioVentaSinImpuesto="getPrecioVentaSinImpuesto"
                @ratioCalculed="setMarkupGFC"
                @onSave="onSaveSubmit"
              />

              <app-ratio-mark-up
                :values="frmMarkupGA"
                :precioVentaSinImpuesto="getPrecioVentaSinImpuesto"
                @ratioCalculed="setMarkupGA"
                @onSave="onSaveSubmit"
              />

              <app-ratio-mark-up
                :values="frmMarkupCLP"
                :precioVentaSinImpuesto="getPrecioVentaSinImpuesto"
                @ratioCalculed="setMarkupCLP"
                :showRatioCalculed=false
                @onSave="onSaveSubmit"
              />

              <app-ratio-mark-up
                :values="frmMarkupI"
                :precioVentaSinImpuesto="getPrecioVentaSinImpuesto"
                @ratioCalculed="setMarkupI"
                :showRatioCalculed=false
                @onSave="onSaveSubmit"
              />

              <app-ratio-mark-up
                :values="frmMarkupOH"
                :precioVentaSinImpuesto="getPrecioVentaSinImpuesto"
                @ratioCalculed="setMarkupOH"
                :showRatioCalculed=false
                @onSave="onSaveSubmit"
              />

              <app-ratio-mark-up
                :values="frmMarkupP"
                :precioVentaSinImpuesto="getPrecioVentaSinImpuesto"
                @ratioCalculed="setMarkupP"
                :showRatioCalculed=false
                @onSave="onSaveSubmit"
              />

              <!-- <app-ratio-mark-up
                :values="frmMarkupFE"
                :precioVentaSinImpuesto="getPrecioVentaSinImpuesto"
                @ratioCalculed="setMarkupFE"
                :showRatioCalculed=false
                @onSave="onSaveSubmit"
              /> -->

              <app-ratio-mark-up
                :values="frmMarkupITFCT"
                :precioVentaSinImpuesto="getPrecioVentaSinImpuesto"
                @ratioCalculed="setMarkupITFCT"
                :showRatioCalculed=false
                @onSave="onSaveSubmit"
              />
              </tbody>
              <tfoot>
                <tr>
                  <th class="text-right">MARK UP=</th>
                  <th class="text-right">{{getMarkup|decimal("0.0000")}}</th>
                  <th></th>
                  <th class="text-right bg-success">TOTAL:</th>
                  <th class="text-right bg-success">{{totalRatioMarkup|decimal("0.0000%")}}</th>
                  <th class="text-right bg-success">{{getTotalMarkup|currency(budget.currency)}}</th>
                  <th></th>
                </tr>
              </tfoot>
            </table>
          </section>

        </b-col>

        <b-col md="4" class="my-1">
            <section class="view-data">
              <table class="table table-striped">
                <col width="40%">
                <col width="15%">
                <col width="15%">
                <col width="15%">
                <col width="15%">
                <thead>
                  <tr>
                    <th class="text-right">PRECIO DE VENTA SIN IMPUESTO</th>
                    <th class="text-right">-</th>
                    <th class="text-right">{{getPrecioVentaSinImpuesto|currency(budget.currency)}}</th>
                  </tr>
                  <tr>
                    <th class="text-right">IMPUESTO AL VALOR AGREGADO</th>
                    <th class="text-right">{{0.18|decimal("0.00%")}}</th>
                    <th class="text-right">{{getIVA|currency(budget.currency)}}</th>
                  </tr>
                  <tr>
                    <th class="text-right">PRECIO DE VENTA CON IGV</th>
                    <th class="text-right">-</th>
                    <th class="text-right">{{getPrecioVentaConIGV|currency(budget.currency)}}</th>
                  </tr>
                  <tr>
                    <th class="text-right">COEFICIENTE DE PASE SIN IVA</th>
                    <th class="text-right">-</th>
                    <th class="text-right">{{getCoeficientePaseSinIVA|decimal("0.0000")}}</th>
                  </tr>
                  <tr>
                    <th class="text-right">COEFICIENTE DE PASE CON IVA</th>
                    <th class="text-right">-</th>
                    <th class="text-right">{{getCoeficientePaseConIVA|decimal("0.0000")}}</th>
                  </tr>
                </thead>
              </table>
            </section>
        </b-col>

        <!-- Fin: Costo indirecto -->
        <b-col md="5" class="my-1">
          <table class="table table-striped">
            <col width="35%">
            <col width="15%">
            <col width="15%">
            <col width="15%">
            <col width="15%">
            <col width="5%">
            <thead>
              <tr>
                <th>Item</th>
                <th>Mano Obra</th>
                <th>Eq. & Herr.</th>
                <th>Material</th>
                <th>Subcontrato</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <app-ratio-markup-diff
                :values="frmMarkupDiffImprevistos"
                @onSave="onSaveSubmit"/>
              <app-ratio-markup-diff
                :values="frmMarkupDiffGastosGenerales"
                @onSave="onSaveSubmit"/>
              <app-ratio-markup-diff
                :values="frmMarkupDiffBeneficio"
                @onSave="onSaveSubmit"/>
            </tbody>
          </table>
        </b-col>
        <b-col md="7" class="my-1">
          <div class="table-responsive">
            <table>
              <col width="10px">
              <col width="100px">
              <col width="100px">
              <col width="20px">
            <thead>
              <tr>
                <th></th>
                <th class="text-right">Gastos Generales</th>
                <th class="text-right">Utilidades</th>
                <th></th>
              </tr>
            </thead>
              <app-ratio-markup-diff
                :values="frmRatioDiff"
                @onSave="onSaveSubmit"/>
            </table>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Item</th>
                  <th>Costo directo</th>
                  <th>Costo Indirecto</th>
                  <th>Costo Industrial</th>
                  <th>Mark Up</th>
                  <th>Venta</th>
                  <th>CP</th>
                  <th>CP sin IVA</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>Costo Mano Obra</th>
                  <td class="text-right">{{getManoObraDirecto|currency(budget.currency)}}</td>
                  <td class="text-right">{{getManoObraIndirecto|currency(budget.currency)}}</td>
                  <td class="text-right">{{getManoObraIndustrial|currency(budget.currency)}}</td>
                  <td class="text-right">{{getManoObraMarkup|decimal("0.00")}}</td>
                  <td class="text-right">{{getManoObraVenta|currency(budget.currency)}}</td>
                  <td class="text-right">{{getManoObraCP|decimal("0.00")}}</td>
                  <td class="text-right">{{getManoObraCPSinIVA|decimal("0.00")}}</td>
                </tr>
                <tr>
                  <th>Costo Eq. & Herr.</th>
                  <td class="text-right">{{getEquipoDirecto|currency(budget.currency)}}</td>
                  <td class="text-right">{{getEquipoIndirecto|currency(budget.currency)}}</td>
                  <td class="text-right">{{getEquipoIndustrial|currency(budget.currency)}}</td>
                  <td class="text-right">{{getEquipoMarkup|decimal("0.00")}}</td>
                  <td class="text-right">{{getEquipoVenta|currency(budget.currency)}}</td>
                  <td class="text-right">{{getEquipoCP|decimal("0.00")}}</td>
                  <td class="text-right">{{getEquipoCPSinIVA|decimal("0.00")}}</td>
                </tr>
                <tr>
                  <th>Costo Materiales</th>
                  <td class="text-right">{{getMaterialDirecto|currency(budget.currency)}}</td>
                  <td class="text-right">{{getMaterialIndirecto|currency(budget.currency)}}</td>
                  <td class="text-right">{{getMaterialIndustrial|currency(budget.currency)}}</td>
                  <td class="text-right">{{getMaterialMarkup|decimal("0.00")}}</td>
                  <td class="text-right">{{getMaterialVenta|currency(budget.currency)}}</td>
                  <td class="text-right">{{getMaterialCP|decimal("0.00")}}</td>
                  <td class="text-right">{{getMaterialCPSinIVA|decimal("0.00")}}</td>
                </tr>
                <tr>
                  <th>Costo Subcontratos</th>
                  <td class="text-right">{{getSubcontratoDirecto|currency(budget.currency)}}</td>
                  <td class="text-right">{{getSubcontratoIndirecto|currency(budget.currency)}}</td>
                  <td class="text-right">{{getSubcontratoIndustrial|currency(budget.currency)}}</td>
                  <td class="text-right">{{getSubcontratoMarkup|decimal("0.00")}}</td>
                  <td class="text-right">{{getSubcontratoVenta|currency(budget.currency)}}</td>
                  <td class="text-right">{{getSubcontratoCP|decimal("0.00")}}</td>
                  <td class="text-right">{{getSubcontratoCPSinIVA|decimal("0.00")}}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <th>Total</th>
                  <th class="text-right">{{getTotalDirecto|currency(budget.currency)}}</th>
                  <th class="text-right">{{getTotalIndirecto|currency(budget.currency)}}</th>
                  <th class="text-right">{{getTotalIndustrial|currency(budget.currency)}}</th>
                  <th class="text-right">-</th>
                  <th class="text-right">{{getTotalVenta|currency(budget.currency)}}</th>
                  <th class="text-right">-</th>
                  <th class="text-right">-</th>
                </tr>
              </tfoot>
            </table>
          </div>
        </b-col>
      </b-row>
    </b-col>

  </b-row>
</template>

<script>
  // import ImportTask from "./task/ImportTask.vue"

  import ManpowerStandBy from "./standby/ManpowerStandBy.vue"
  import EquipmentStandBy from "./standby/EquipmentStandBy.vue"
  import { mapState } from 'vuex'
  import Title from "../utils/Title.vue"
  import ScheduledCompletion from "./closed/ScheduledCompletion.vue"
  import RatioMarkUp from "./closed/RatioMarkUp.vue"
  import RatioBudget from "./closed/RatioBudget.vue"
  import RatioMarkupDiff from "./closed/RatioMarkupDiff.vue"
  import RatioMarkUpDiff2 from "./closed/RatioMarkUpDifferentiated.vue"
  // import jQuery from 'jquery'
  // import {RotateSquare2} from 'vue-loading-spinner'

  const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    }

  const url_api = `/budget/api/budgets/`
  var numeral = require('numeral')
  export default {
      components: {
        'app-title': Title,
        'app-scheduledcompletion': ScheduledCompletion,
        'app-ratio-mark-up': RatioMarkUp,
        'app-ratio-budget': RatioBudget,
        'app-ratio-markup-diff': RatioMarkupDiff,
        'app-ratio-mark-up-diff2': RatioMarkUpDiff2,
      },
      data() {
        return {
          // refreshApu: false,
          // budget: "",
          manpowers: "",
          workshops: "",
          medicals: "",
          equipments: "",
          operatives: "",
          various: "",
          standby: "",
          markupGFC: -1,
          markupGA: -1,
          markupCLP: -1,
          markupI: -1,
          markupOH: -1,
          markupP: -1,
          markupFE: -1,
          markupITFCT: -1,
          direct: {
              total: 0,
              items: {
                  manpowers: 0,
                  equipments: 0,
                  materials: 0,
                  subcontract: 0,
                  min_tools: 0,
              }
          },
          editingScheduledCompletion: false,
          formRatioBudget: {
            ratio_manpower: 0,
            ratio_material: 0,
            ratio_equipment: 0,
            ratio_subcontract: 0,
          },
          formScheduledCompletion: {
            scheduled_completion: 0,
            scheduled_completion_extra: 0,
            get_period_faithful_compliance: 0,
            ratio_guarantee_faithful_compliance: 0,
            ratio2_guarantee_faithful_compliance: 0,
            get_period_guarantee_faithful_compliance: 0,
            get_ratio_guarantee_faithful_compliance: 0
          },
          frmMarkupGFC: {
            label: 'Emisión de Carta de Fianza de Fiel Cumplimiento',
            price: 0,
            fields: [
              {key: 'ratio_guarantee_faithful_compliance', editable: true, format: "0.0000%", visible: true},
              {key: 'get_period_guarantee_faithful_compliance', editable: false, format: "0", visible: true},
              {key: 'ratio2_guarantee_faithful_compliance', editable: true, format: "0.00%", visible: true},
            ],
            items: {
              ratio_guarantee_faithful_compliance: 0,
              ratio2_guarantee_faithful_compliance: 0,
              get_period_guarantee_faithful_compliance: 0
            }
          },
          frmMarkupGA: {
            label: 'Emisión de Carta de Fianza por Adelanto',
            price: 0,
            fields: [
              {key: 'ratio_guarantee_advance', editable: true, format: "0.0000%", visible: true},
              {key: 'get_period_guarantee_advance', editable: false, format: "0", visible: true},
              {key: 'ratio2_guarantee_advance', editable: true, format: "0.00%", visible: true},
            ],
            items: {
              ratio_guarantee_advance: 0,
              ratio2_guarantee_advance: 0,
              get_period_guarantee_advance: 0
            }
          },
          frmMarkupCLP: {
            label: 'Poliza de responsabilidad civil',
            fields: [
              {key: 'col1', editable: false, visible: true, isFalse: true},
              {key: 'col2', editable: false, visible: true, isFalse: true},
              {key: 'col3', editable: false, visible: true, isFalse: true},
              {key: 'ratio_civil_liability_policy', editable: true, format: "0.0000%", visible: true},
            ],
            items: {
              ratio_civil_liability_policy: 0,
            }
          },
          frmMarkupI: {
            label: 'Imprevistos',
            fields: [
              {key: 'col1', editable: false, visible: true, isFalse: true},
              {key: 'col2', editable: false, visible: true, isFalse: true},
              {key: 'col3', editable: false, visible: true, isFalse: true},
              {key: 'ratio_incidentals', editable: true, format: "0.0000%", visible: true},
            ],
            items: {
              ratio_incidentals: 0,
            }
          },
          frmMarkupOH: {
            label: 'Gastos Generales',
            fields: [
              {key: 'col1', editable: false, visible: true, isFalse: true},
              {key: 'col2', editable: false, visible: true, isFalse: true},
              {key: 'col3', editable: false, visible: true, isFalse: true},
              {key: 'ratio_over_head', editable: true, format: "0.0000%", visible: true},
            ],
            items: {
              ratio_over_head: 0,
            }
          },
          frmMarkupP: {
            label: 'Beneficio',
            fields: [
              {key: 'col1', editable: false, visible: true, isFalse: true},
              {key: 'col2', editable: false, visible: true, isFalse: true},
              {key: 'col3', editable: false, visible: true, isFalse: true},
              {key: 'ratio_profit', editable: true, format: "0.0000%", visible: true},
            ],
            items: {
              ratio_profit: 0,
            }
          },
          frmMarkupFE: {
            label: 'Gastos Financieros',
            fields: [
              {key: 'col1', editable: false, visible: true, isFalse: true},
              {key: 'col2', editable: false, visible: true, isFalse: true},
              {key: 'col3', editable: false, visible: true, isFalse: true},
              {key: 'ratio_financial_expenses', editable: true, format: "0.0000%", visible: true},
            ],
            items: {
              ratio_financial_expenses: 0,
            }
          },
          frmMarkupITFCT: {
            label: 'Impuestos cheque ITF',
            fields: [
              {key: 'col1', editable: false, visible: true, isFalse: true},
              {key: 'col2', editable: false, visible: true, isFalse: true},
              {key: 'col3', editable: false, visible: true, isFalse: true},
              {key: 'ratio_itf_check_tax', editable: true, format: "0.0000%", visible: true},
            ],
            items: {
              ratio_itf_check_tax: 0,
            }
          },
          frmMarkupDiffImprevistos: {
            label: 'Imprevistos',
            fields: [
              {key: 'ratio_incidentals_manpowers', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_incidentals_equipments', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_incidentals_materials', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_incidentals_subcontracts', editable: true, format: "0.00%", visible: true},
            ],
            items: {
              ratio_incidentals_manpowers: 0.03,
              ratio_incidentals_equipments: 0.03,
              ratio_incidentals_materials: 0.03,
              ratio_incidentals_subcontracts: 0.03,
            }
          },
          frmMarkupDiffGastosGenerales: {
            label: 'Gastos Generales',
            fields: [
              {key: 'ratio_over_head_manpowers', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_over_head_equipments', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_over_head_materials', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_over_head_subcontracts', editable: true, format: "0.00%", visible: true},
            ],
            items: {
              ratio_over_head_manpowers: 0.1,
              ratio_over_head_equipments: 0.1,
              ratio_over_head_materials: 0.1,
              ratio_over_head_subcontracts: 0.1,
            }
          },
          frmMarkupDiffBeneficio: {
            label: 'Beneficio',
            fields: [
              {key: 'ratio_profit_manpowers', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_profit_equipments', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_profit_materials', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_profit_subcontracts', editable: true, format: "0.00%", visible: true},
            ],
            items: {
              ratio_profit_manpowers: 0.1,
              ratio_profit_equipments: 0.1,
              ratio_profit_materials: 0.1,
              ratio_profit_subcontracts: 0.1,
            }
          },
          frmRatioDiff: {
            label: '',
            fields: [
              {key: 'ratio_gastos_generales_diff', editable: true, format: "0.00%", visible: true},
              {key: 'ratio_utilidad_diff', editable: true, format: "0.00%", visible: true},
            ],
            items: {
              ratio_gastos_generales_diff: 0,
              ratio_utilidad_diff: 0
            }
          },
          formMarkUpDifferentiated: {
            ratio_incidentals_manpowers: 0,
            ratio_incidentals_equipments: 0,
            ratio_incidentals_materials: 0,
            ratio_incidentals_subcontracts: 0,
            ratio_over_head_manpowers: 0,
            ratio_over_head_materials: 0,
            ratio_over_head_equipments: 0,
            ratio_over_head_subcontracts: 0,
            ratio_profit_manpowers: 0,
            ratio_profit_materials: 0,
            ratio_profit_equipments: 0,
            ratio_profit_subcontracts: 0,
          }
        }
      },
      computed:{
        budget(){
          return this.$store.getters['budget/getSelectedBudget']
        },
        getManoObraDirecto(){
          return this.direct.items.manpowers/this.formRatioBudget.ratio_manpower
        },
        getEquipoDirecto(){
          return (this.direct.items.equipments+this.direct.items.min_tools)/this.formRatioBudget.ratio_equipment
        },
        getMaterialDirecto(){
          return (this.direct.items.materials/this.formRatioBudget.ratio_material)
        },
        getSubcontratoDirecto(){
          return (this.direct.items.subcontracts/this.formRatioBudget.ratio_subcontract)
        },
        getTotalDirecto(){
          var total=0
          if (this.getManoObraDirecto>0){
            total = total + this.getManoObraDirecto
          }
          if (this.getEquipoDirecto>0) {
            total = total + this.getEquipoDirecto
          }

          if (this.getMaterialDirecto>0) {
            total = total + this.getMaterialDirecto
          }

          if (this.getSubcontratoDirecto>0){
            total = total + this.getSubcontratoDirecto
          }
          return total
        },
        getManoObraIndirecto(){
          return this.totalIndirect * this.getRatio(this.direct.items.manpowers, this.direct.total)
        },
        getEquipoIndirecto(){
          return this.totalIndirect * this.getRatio((this.direct.items.equipments + this.direct.items.min_tools), this.direct.total)
        },
        getMaterialIndirecto(){
          return this.totalIndirect * this.getRatio(this.direct.items.materials, this.direct.total)
        },
        getSubcontratoIndirecto(){
          return this.totalIndirect * this.getRatio(this.direct.items.subcontracts, this.direct.total)
        },
        getTotalIndirecto(){
          // console.log("this.getManoObraDirecto", this.getManoObraDirecto)
          var total=0
          if (this.getManoObraIndirecto>0){
            total = total + this.getManoObraIndirecto
          }
          if (this.getEquipoIndirecto>0) {
            total = total + this.getEquipoIndirecto
          }

          if (this.getMaterialIndirecto>0) {
            total = total + this.getMaterialIndirecto
          }

          if (this.getSubcontratoIndirecto>0){
            total = total + this.getSubcontratoIndirecto
          }
          return total
        },
        getManoObraIndustrial(){
          return (this.direct.items.manpowers/this.formRatioBudget.ratio_manpower)+this.getManoObraIndirecto
        },
        getEquipoIndustrial(){
          return ((this.direct.items.equipments+this.direct.items.min_tools)/this.formRatioBudget.ratio_equipment)+this.getEquipoIndirecto
        },
        getMaterialIndustrial(){
          return (this.direct.items.materials/this.formRatioBudget.ratio_material)+this.getMaterialIndirecto
        },
        getSubcontratoIndustrial(){
          return (this.direct.items.subcontracts/this.formRatioBudget.ratio_subcontract)+this.getSubcontratoIndirecto
        },
        getTotalIndustrial(){
          // console.log("this.getManoObraDirecto", this.getManoObraDirecto)
          var total=0
          if (this.getManoObraIndustrial>0){
            total = total + this.getManoObraIndustrial
          }
          if (this.getEquipoIndustrial>0) {
            total = total + this.getEquipoIndustrial
          }

          if (this.getMaterialIndustrial>0) {
            total = total + this.getMaterialIndustrial
          }

          if (this.getSubcontratoIndustrial>0){
            total = total + this.getSubcontratoIndustrial
          }
          return total
        },
        getManoObraMarkup(){
          let total = 0.00
          if (this.markupGFC>-1){
            total = total + this.markupGFC
          }
          if (this.markupGA>-1){
            total = total + parseFloat(this.markupGA)
          }
          if (this.markupCLP>-1){
            total = total + parseFloat(this.markupCLP)
          }
          if (this.markupITFCT>-1){
            total = total + parseFloat(this.markupITFCT)
          }
          if (total>0){
            total = total + parseFloat(this.budget.ratio_incidentals_manpowers) + parseFloat(this.budget.ratio_over_head_manpowers) + parseFloat(this.budget.ratio_profit_manpowers)
          }

          return 1/(1-(total))
        },
        getEquipoMarkup(){
          let total = 0.00
          if (this.markupGFC>-1){
            total = total + this.markupGFC
          }
          if (this.markupGA>-1){
            total = total + parseFloat(this.markupGA)
          }
          if (this.markupCLP>-1){
            total = total + parseFloat(this.markupCLP)
          }
          if (this.markupITFCT>-1){
            total = total + parseFloat(this.markupITFCT)
          }
          if (total>0){
            total = total + parseFloat(this.budget.ratio_incidentals_equipments) + parseFloat(this.budget.ratio_over_head_equipments) + parseFloat(this.budget.ratio_profit_equipments)
          }
          return 1/(1-(total))
        },
        getMaterialMarkup(){
          let total = 0.00
          if (this.markupGFC>-1){
            total = total + this.markupGFC
          }
          if (this.markupGA>-1){
            total = total + parseFloat(this.markupGA)
          }
          if (this.markupCLP>-1){
            total = total + parseFloat(this.markupCLP)
          }
          if (this.markupITFCT>-1){
            total = total + parseFloat(this.markupITFCT)
          }
          if (total>0){
            total = total + parseFloat(this.budget.ratio_incidentals_materials) + parseFloat(this.budget.ratio_over_head_materials) + parseFloat(this.budget.ratio_profit_materials)
          }
          return 1/(1-(total))
        },
        getSubcontratoMarkup(){
          let total = 0.00
          if (this.markupGFC>-1){
            total = total + this.markupGFC
          }
          if (this.markupGA>-1){
            total = total + parseFloat(this.markupGA)
          }
          if (this.markupCLP>-1){
            total = total + parseFloat(this.markupCLP)
          }
          if (this.markupITFCT>-1){
            total = total + parseFloat(this.markupITFCT)
          }
          if (total>0){
            total = total + parseFloat(this.budget.ratio_incidentals_subcontracts) + parseFloat(this.budget.ratio_over_head_subcontracts) + parseFloat(this.budget.ratio_profit_subcontracts)
          }
          return 1/(1-(total))
        },
        getManoObraVenta(){
          return this.getManoObraIndustrial * this.getManoObraMarkup
        },
        getEquipoVenta(){
          return this.getEquipoIndustrial * this.getEquipoMarkup
        },
        getMaterialVenta(){
          return this.getMaterialIndustrial * this.getMaterialMarkup
        },
        getSubcontratoVenta(){
          return this.getSubcontratoIndustrial * this.getSubcontratoMarkup
        },
        getTotalVenta(){
          let total = 0
          if (this.getManoObraVenta>0){
            total += this.getManoObraVenta
          }
          if (this.getEquipoVenta>0){
            total += this.getEquipoVenta
          }
          if (this.getMaterialVenta>0){
            total += this.getMaterialVenta
          }
          if (this.getSubcontratoVenta>0){
            total += this.getSubcontratoVenta
          }
          return total
        },
        getManoObraCP(){
          return this.getManoObraVenta / this.getManoObraDirecto
        },
        getEquipoCP(){
          return this.getEquipoVenta / this.getEquipoDirecto
        },
        getMaterialCP(){
          return this.getMaterialVenta / this.getMaterialDirecto
        },
        getSubcontratoCP(){
          return this.getSubcontratoVenta / this.getSubcontratoDirecto
        },
        getManoObraCPSinIVA(){
          let total=0
          if (this.getManoObraCP>0){
            total = parseFloat(this.getManoObraCP) / (1 + parseFloat(this.frmRatioDiff.items.ratio_gastos_generales_diff) + parseFloat(this.frmRatioDiff.items.ratio_utilidad_diff))
          }
          return total
        },
        getEquipoCPSinIVA(){
          let total=0
          if (this.getEquipoCP>0){
            total = parseFloat(this.getEquipoCP) / (1 + parseFloat(this.frmRatioDiff.items.ratio_gastos_generales_diff) + parseFloat(this.frmRatioDiff.items.ratio_utilidad_diff))
          }
          return total
        },
        getMaterialCPSinIVA(){
          let total=0
          if (this.getMaterialCP>0){
            total = parseFloat(this.getMaterialCP) / (1 + parseFloat(this.frmRatioDiff.items.ratio_gastos_generales_diff) + parseFloat(this.frmRatioDiff.items.ratio_utilidad_diff))
          }
          return total
        },
        getSubcontratoCPSinIVA(){
          let total=0
          if (this.getSubcontratoCP>0){
            total = parseFloat(this.getSubcontratoCP) / (1 + parseFloat(this.frmRatioDiff.items.ratio_gastos_generales_diff) + parseFloat(this.frmRatioDiff.items.ratio_utilidad_diff))
          }
          return total
        },

        totalRatioMarkup(){
          var total = 0
          if (this.markupGFC>-1){
            total = total + this.markupGFC
          }
          if (this.markupGA>-1){
            total = total + this.markupGA
          }
          if (this.markupCLP>-1){
            total = total + this.markupCLP
          }
          if (this.markupI>-1){
            total = total + this.markupI
          }
          if (this.markupOH>-1){
            total = total + this.markupOH
          }
          if (this.markupP>-1){
            total = total + this.markupP
          }
          if (this.markupFE>-1){
            total = total + this.markupFE
          }
          if (this.markupITFCT>-1){
            total = total + this.markupITFCT
          }
          return total
        },
        getTotalMarkup(){
          return this.totalRatioMarkup * this.getPrecioVentaSinImpuesto
        },
        getMarkup(){
          return 1/(1-this.totalRatioMarkup)
        },
        getPrecioVentaSinImpuesto(){
          return this.getMarkup * this.totalCostIndustry
        },
        getIVA(){
          return this.getPrecioVentaSinImpuesto * 0.18
        },
        getPrecioVentaConIGV(){
          return this.getPrecioVentaSinImpuesto + this.getIVA
        },
        getCoeficientePaseSinIVA(){
          return this.getPrecioVentaSinImpuesto / this.direct.total
        },
        getCoeficientePaseConIVA(){
          return this.getPrecioVentaConIGV / this.direct.total
        },
        totalDirect(){
          let total = 0
          if (this.direct && this.direct.items){
            total = this.direct.items.manpowers
          }
          return total
        },
        totalIndirect(){
          const total = this.manpowers.total + this.totalStandby + this.workshops.total + this.operatives.total + this.medicals.total + this.various.total
          return total
        },
        totalStandby(){
          return this.standby.manpower + this.standby.equipment
        },
        totalCostIndustry(){
          return this.direct.total + this.totalIndirect
        }
      },
      created() {
        this.budgetId = this.$route.params.budget
        // if(this.$route.query.task){
        //   this.taskId = this.$route.query.task
        //   this.getTask()
        // }
        this.$store.dispatch('budget/requestBudgetInformation', this.$route.params.budget)
      },
      watch: {
        budget(){
          this.getBudget()
        }
      },
      methods: {
        setMarkupGFC(data){
          this.markupGFC = data
        },
        setMarkupGA(data){
          this.markupGA = data
        },
        setMarkupCLP(data){
          this.markupCLP = data
        },
        setMarkupI(data){
          this.markupI = data
        },
        setMarkupOH(data){
          this.markupOH = data
        },
        setMarkupP(data){
          this.markupP = data
        },
        setMarkupFE(data){
          this.markupFE = data
        },
        setMarkupITFCT(data){
          this.markupITFCT = data
        },
        editScheduledCompletion(){
          this.editingScheduledCompletion = true
        },
        onSaveSubmit(data){
          // evt.preventDefault()
          // var isValid = this.$refs.vfg.validate()
          // if(isValid){
            data.id = this.budgetId
            this.$store.dispatch(`budget/updateBudget`, data).then(response => {
              this.$swal({
                position: 'top-end',
                toast: true,
                type: 'success',
                title: `Se ${this.mode=='add' ? 'agregó': 'actualizó'} correctamente.`,
                showConfirmButton: false,
                timer: 1500
              })
              // this.$store.dispatch('budget/requestBudgets')
              // this.$refs.modalForm.hide()
            }, error =>{
                var msgError = ""
                console.log("Error>>>", error)
                Object.keys(error.body).forEach((element) => {
                  msgError += `${element} : ${error.body[element]}\n`
                });
                this.$swal({
                  type: 'error',
                  title: 'Oops...',
                  text: 'Error, no se pudo guardar\n' + msgError
                })
            })
          // }
        },
        // onSaveSubmit(data) {
        //   let url = `/budget/api/budgets/${this.budgetId}/`
        //   let vm = this
        //   // console.log("data:", data)
        //   this.$http.patch(url, data)
        //     .then((response) => {
        //       this.$swal({
        //         position: 'top-end',
        //         toast: true,
        //         type: 'success',
        //         title: 'Se guardó correctamente.',
        //         showConfirmButton: false,
        //         timer: 1500
        //       })
        //       // vm.$store.dispatch('requestTaskInformation', vm.task.id)
        //       this.getBudget()
        //     })
        //     .catch((err) => {
        //       // console.log("error:", err)
        //       var msgError = ""
        //       Object.getOwnPropertyNames(err.body).forEach((element) => {
        //         msgError += `${element} : ${err.body[element]}\n`
        //       });
        //       this.$swal({
        //         type: 'error',
        //         title: 'Oops...',
        //         text: 'Error, no se pudo guardar\n' + msgError
        //       })
        //     })
        // },
        showRatioBudgetModal(){
          this.formRatioBudget = {
            ratio_manpower: this.budget.ratio_manpower,
            ratio_material: this.budget.ratio_material,
            ratio_equipment: this.budget.ratio_equipment,
            ratio_subcontract: this.budget.ratio_subcontract,
          }
          this.$refs.modalRatioBudget.show()
        },
        getRatio(numerator, denominator ){
          return numerator / denominator
        },
        updatedMaterial(){
          this.getMaterials('W') // Taller
          this.getMaterials('M') // Medico
          this.getMaterials('O') // Otros
          this.getMaterials('V') // Varios
        },
        getBudget(){
          // let url = `${url_api}${this.budgetId}/`
          // this.$http.get(url)
          //   .then((response) => {
                // this.budget = response.data
                this.formRatioBudget = {
                  ratio_manpower: this.budget.ratio_manpower,
                  ratio_material: this.budget.ratio_material,
                  ratio_equipment: this.budget.ratio_equipment,
                  ratio_subcontract: this.budget.ratio_subcontract,
                }
                this.formScheduledCompletion = {
                  scheduled_completion: this.budget.scheduled_completion,
                  scheduled_completion_extra: this.budget.scheduled_completion_extra,
                  get_period_faithful_compliance: this.budget.get_period_faithful_compliance
                }
                this.formMarkUpDifferentiated = {
                  ratio_incidentals_manpowers: this.budget.ratio_incidentals_manpowers,
                  ratio_incidentals_equipments: this.budget.ratio_incidentals_equipments,
                  ratio_incidentals_materials: this.budget.ratio_incidentals_materials,
                  ratio_incidentals_subcontracts: this.budget.ratio_incidentals_subcontracts,
                  ratio_over_head_manpowers: this.budget.ratio_over_head_manpowers,
                  ratio_over_head_materials: this.budget.ratio_over_head_materials,
                  ratio_over_head_equipments: this.budget.ratio_over_head_equipments,
                  ratio_over_head_subcontracts: this.budget.ratio_over_head_subcontracts,
                  ratio_profit_manpowers: this.budget.ratio_profit_manpowers,
                  ratio_profit_materials: this.budget.ratio_profit_materials,
                  ratio_profit_equipments: this.budget.ratio_profit_equipments,
                  ratio_profit_subcontracts: this.budget.ratio_profit_subcontracts
                }
                this.frmMarkupGFC.items = {
                  ratio_guarantee_faithful_compliance: this.budget.ratio_guarantee_faithful_compliance,
                  ratio2_guarantee_faithful_compliance: this.budget.ratio2_guarantee_faithful_compliance,
                  get_period_guarantee_faithful_compliance: this.budget.get_period_guarantee_faithful_compliance
                }
                this.frmMarkupGA.items = {
                  ratio_guarantee_advance: this.budget.ratio_guarantee_advance,
                  ratio2_guarantee_advance: this.budget.ratio2_guarantee_advance,
                  get_period_guarantee_advance: this.budget.get_period_guarantee_advance
                }
                this.frmMarkupCLP.items = {
                  ratio_civil_liability_policy: this.budget.ratio_civil_liability_policy
                }
                this.frmMarkupI.items = {
                  ratio_incidentals: this.budget.ratio_incidentals
                }
                this.frmMarkupOH.items = {
                  ratio_over_head: this.budget.ratio_over_head
                }
                this.frmMarkupP.items = {
                  ratio_profit: this.budget.ratio_profit
                }
                this.frmMarkupFE.items = {
                  ratio_financial_expenses: this.budget.ratio_financial_expenses
                }
                this.frmMarkupITFCT.items = {
                  ratio_itf_check_tax: this.budget.ratio_itf_check_tax
                }
                this.$set(this.frmMarkupDiffImprevistos.items,
                  'ratio_incidentals_manpowers', this.budget.ratio_incidentals_manpowers)
                // this.frmMarkupDiffImprevistos.items = {
                //   ratio_incidentals_manpowers: this.budget.ratio_incidentals_manpowers,
                //   ratio_incidentals_equipments: this.budget.ratio_incidentals_equipments,
                //   ratio_incidentals_materials: this.budget.ratio_incidentals_materials,
                //   ratio_incidentals_subcontracts: this.budget.ratio_incidentals_subcontracts
                // }
                this.frmMarkupDiffGastosGenerales.items = {
                  ratio_over_head_manpowers: this.budget.ratio_over_head_manpowers,
                  ratio_over_head_equipments: this.budget.ratio_over_head_equipments,
                  ratio_over_head_materials: this.budget.ratio_over_head_materials,
                  ratio_over_head_subcontracts: this.budget.ratio_over_head_subcontracts
                }
                this.frmMarkupDiffBeneficio.items = {
                  ratio_profit_manpowers: this.budget.ratio_profit_manpowers,
                  ratio_profit_equipments: this.budget.ratio_profit_equipments,
                  ratio_profit_materials: this.budget.ratio_profit_materials,
                  ratio_profit_subcontracts: this.budget.ratio_profit_subcontracts
                }
                this.frmRatioDiff.items = {
                  ratio_gastos_generales_diff: this.budget.ratio_gastos_generales_diff,
                  ratio_utilidad_diff: this.budget.ratio_utilidad_diff
                }
                this.getManpowerOverhead()
                this.getStandby()
                this.getMaterials('W')
                this.getMaterials('M')
                this.getMaterials('O')
                this.getMaterials('V')
                this.getDirectCosts()
            // })
            // .catch((err) => {
            //   console.log("error en getBudget", err)
            // })
        },
        getStandby(){
          let url = `/budget/api/budgets/${this.budgetId}/standby/overhead`
          this.$http.get(url)
            .then((response) => {
              this.standby = response.data
            })
            .catch((err) => {
              console.log("error en getStandBy::", err)
            })
        },
        getMaterials(typeMaterial){
          let url = `/budget/api/budgets/${this.budgetId}/material/${typeMaterial}/overhead`
          this.$http.get(url)
            .then((response) => {
              if(typeMaterial=="W"){
                this.workshops = response.data
              }
              if(typeMaterial=="M"){
                this.medicals = response.data
              }
              if(typeMaterial=="O"){
                this.operatives = response.data
              }
              if(typeMaterial=="V"){
                this.various = response.data
              }
            })
            .catch((err) => {
              console.log("error en getMaterialBudget::", err)
            })
        },
        getManpowerOverhead(){
          let url = `/budget/api/budgets/${this.budgetId}/manpower/overhead`
          this.$http.get(url)
            .then((response) => {
              this.manpowers = response.data
            })
            .catch((err) => {
              console.log("error en getManpowerBudget::", err)
            })
        },
        getDirectCosts(){
          let url = `/budget/api/budgets/${this.budgetId}/direct/close`
          this.$http.get(url)
            .then((response) => {
              this.direct = response.data
            })
            .catch((err) => {
              console.log("error en getDirectCosts::", err)
            })
        },
      },
  }
</script>
