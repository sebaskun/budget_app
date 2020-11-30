var status_budget = {
    "WA": {
        "color": "info",
        "icon": "alarm"
    },
    "NW": {
        "color": "success",
        "icon": "alert-octagon"
    },
    "SU": {
        "color": "primary",
        "icon": "check"
    },
    "CA": {
        "color": "warning",
        "icon": "close-circle"
    },
    "TC": {
        "color": "secondary",
        "icon": "calendar-clock"
    },
    "UD": {
        "color": "dark",
        "icon": "infinity"
    }
}



// Vue.component('select2', {
//   props: ['options', 'value'],
//   template: '#select2-template',
//   mounted: function () {
//     var vm = this
//     $(this.$el)
//       // init select2
//       .select2({ data: this.options })
//       .val(this.value)
//       .trigger('change')
//       // emit event on change.
//       .on('change', function () {
//         vm.$emit('input', this.value)
//       })
//   },
//   watch: {
//     value: function (value) {
//       // update value
//       $(this.$el).val(value)
//     },
//     options: function (options) {
//       // update options
//       $(this.$el).empty().select2({ data: options })
//     }
//   },
//   destroyed: function () {
//     $(this.$el).off().select2('destroy')
//   }
// })

