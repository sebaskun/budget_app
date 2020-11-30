// using jQuery

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
Vue.http.headers.common['X-CSRFToken'] = csrftoken;

Vue.use(VTooltip);
Vue.component('v-select', VueSelect.VueSelect);
Vue.component('edit-grid', {
  template: '#edit-grid-template',
  delimiters: ['$#', '#'],
  props: {
    data: Array,
    columns: Array,
    columns_title: Array,
    widths: Array,
    filterKey: String,
    edit_function: Function,
    delete_function: Function,
    fields_link: Array,
    color_function: Function,
    status_list: Array,
    status_edit_function: Function,
  },
  data: function () {
    var sortOrders = {}
    this.columns.forEach(function (key) {
      sortOrders[key] = 1
    })
    return {
      sortKey: '',
      sortOrders: sortOrders
    }
  },
  computed: {
    filteredData: function () {
      var sortKey = this.sortKey
      var filterKey = this.filterKey && this.filterKey.toLowerCase()
      var order = this.sortOrders[sortKey] || 1
      var data = this.data
      if (filterKey) {
        data = data.filter(function (row) {
          return Object.keys(row).some(function (key) {
            return String(row[key]).toLowerCase().indexOf(filterKey) > -1
          })
        })
      }
      if (sortKey) {
        data = data.slice().sort(function (a, b) {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return data
    }
  },
  filters: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    },
    /*formatDate: function (value) {
      if (value) {
        return moment(String(value), "YYYY-MM-DD").format('DD/MM/YYYY')
      }
    }*/
  },
  methods: {
    sortBy: function (key) {
      this.sortKey = key
      this.sortOrders[key] = this.sortOrders[key] * -1
    },
  },
})

const new_budget = {
  "code": null,
  "title": null,
  "client": null,
  "summary": null,
  "currency": "D",
  "deadline": null,
  "base_amount": 0.0,
  "exchange_rate": 1.0,
}

new Vue({
      el: '#app',
      delimiters: ['$#', '#'],
      data: {
        searchQuery: '',
        statusList: [],
        selectedStatus: "",
        gridColumns: ['code', 'title', 'get_client', 'deadline'],
        gridColumnsTitle: ['código', 'Título', 'Cliente', 'Fecha'],
        widthColumns: [1,6,3,1],
        fieldsLink: ["code", "title"],
        budgetList: [],
        clientList: [],
        selectedClient: "",
        loading: true,
        errors: [],
        selectedBudget: {},
        newBudget: new_budget,
      },
      mounted: function() {
        this.getBudgetList();
        this.getStatusList();
        this.getClients();
      /*          var vm = this*/
        // $('.datepicker').datepicker({
        //   format: 'yyyy-mm-dd',
        //   autoclose: true,
        //   todayHighlight: true,
        //   onSelect: function(dateText) {
        //     console.log("****", dateText);
        //     /*vm.deadline = dateText*/
        //   }
        // })
      },
      methods: {
        getIcon: function(code){
          return status_budget[code].icon
        },
        getColor: function(code){
          return status_budget[code].color
        },
        // getStatusName: function(code){
        //   return statusList.find(item=>{item.code == code}).name
        // },
        getClients: function() {
          this.loading = true;
          this.$http.get('/client/api/clients/')
              .then((response) => {
                this.clientList = response.data.results;
                this.loading = false;
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })

        },
        // padding_left: function(level){
        //   return "pad_left_" + level
        // },
        getBudgetList: function() {
          this.loading = true;
          this.$http.get('/budget/api/budgets/')
              .then((response) => {
                this.budgetList = response.data.results;
                this.loading = false;
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        getStatusList: function() {
          this.loading = true;
          this.$http.get('/budget/api/status/')
              .then((response) => {
                this.statusList = response.data;
                this.loading = false;
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        getBudget: function(id) {
          this.loading = true;
          this.$http.get(`/budget/api/budgets/${id}/`)
              .then((response) => {
                this.selectedBudget = response.data;
                this.selectedClient = this.clientList.find(item => item.id === this.selectedBudget.client);
                $("#editModelModal").modal('show');
                $("#title").focus();
                this.loading = false;
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        getStatusBudget: function(id) {
          this.loading = true;
          this.$http.get(`/budget/api/budgets/${id}/`)
              .then((response) => {
                this.selectedBudget = response.data;
                this.selectedStatus = this.statusList.find(item => item.code === this.selectedBudget.status);
                $("#statuseditModal").modal('show');
                this.loading = false;
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        updateBudget: function() {
          this.loading = true;
          this.selectedBudget.client = this.selectedClient.id;
          this.$http.put(`/budget/api/budgets/${this.selectedBudget.id}/`, this.selectedBudget)
              .then((response) => {
                this.loading = false;
                this.selectedBudget = response.data;
                $("#editModelModal").modal('hide');
                this.errors = [],
                this.getBudgetList();
              })
              .catch((err) => {
                this.loading = false;
                this.errors = [],
                this.errors.push(err.body);
                console.log("error>>>", err);
              })
        },
        updateStatusBudget: function() {
          this.loading = true;
          this.selectedStatusBudget = this.selectedStatus.code;
          this.$http.put(`/budget/api/budgets/${this.selectedBudget.id}/`, {"status": this.selectedStatus.code})
              .then((response) => {
                this.loading = false;
                this.selectedBudget = response.data;
                $("#statuseditModal").modal('hide');
                this.errors = [],
                this.getBudgetList();
                this.getStatusList();
              })
              .catch((err) => {
                this.loading = false;
                this.errors = [],
                this.errors.push(err.body);
                console.log("error>>>", err);
              })
        },
        addBudget: function() {
          this.loading = true;
          this.newBudget.client = this.selectedClient.id;
          this.$http.post(`/budget/api/budgets/`,this.newBudget)
              .then((response) => {
                this.loading = false;
                this.errors = [],
                $("#addModelModal").modal('hide');
                this.newBudget = new_budget,
                this.getBudgetList();
                this.getStatusList();
              })
              .catch((err) => {
                this.loading = false;
                this.errors = [],
                this.errors.push(err.body);
                console.log("error>>>", err);
              })
        },
        deleteBudget: function(obj) {
              swal({
                title: "¿Está seguro de borrar?",
                text: obj.nombre + ", será borrado.",
                icon: "warning",
                buttons: ["Cancelar", "Borrar"],
                // button: "Borrar",
                dangerMode: true,
              })
              .then((willDelete) => {
                if (willDelete) {
                  this.loading = true;
                  this.$http.delete(`/api/budgets/${obj.id}/`)
                      .then((response) => {
                        this.loading = false;
                        this.getModels();
                      })
                      .catch((err) => {
                        this.loading = false;
                        console.log(err);
                      });
                }
              });
        },
      },
    },
  )
