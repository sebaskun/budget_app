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

Vue.http.headers.common['X-CSRFToken'] = getCookie('csrftoken');

Vue.use(VTooltip);
Vue.component('v-select', VueSelect.VueSelect);

// define the item component
Vue.component('item', {
  template: '#item-template',
  delimiters: ['$#', '#'],
  // props: {
  //   model: Object,
  //   update_function: Function,
  //   show_dates: Function,
  // },
  props: [
    "model",
    "update_function",
    "show_dates",
    "edit_apu"
  ],
  data: function () {
    return {
      open: true
    }
  },
  computed: {
    isFolder: function () {
      return this.model.get_children &&
        this.model.get_children.length
    }
  },
  methods: {
    toggle: function () {
      if (this.isFolder) {
        this.open = !this.open
      }
    },
  },
  filters: {
    currency: function (str, curr="D") {
      symbol = {'S': 'S/', 'D': "$"}
      return symbol[curr] + " " + numeral(str).format('0,0.00');
    }
  }
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

const task_msp = {
  "uid": null,
  "id": null,
  "name": null,
  "active": null,
  "manual": null,
  "wbs": null,
  "outlinelevel": null,
  "priority": null,
  "start": null,
  "finish": null,
  "remainingduration": null,
}

const task_model = {
  "id": null,
  "budget": null,
  "wbs": null,
  "name": null,
  "unit": null,
  "efficiency": null,
  "quantity": null,
  "projected_start_date": null,
  "projected_finish_date": null,
  "moneda": null,
  "subtotal": null,
  "position": null,
  "get_children": null,
}

var $tasks_xml;

var fr = new FileReader(); // FileReader instance
var file;
var vm = new Vue({
      el: '#app',
      delimiters: ['$#', '#'],
      data: {
        // budgetList: [],
        // clientList: [],
        showCalendar: show_calendar,
        currentTask: {},
        errors: [],
        fieldsLink: ["code", "title"],
        file: null,
        // gridColumns: ['code', 'title', 'get_client', 'deadline'],
        // gridColumnsTitle: ['código', 'Título', 'Cliente', 'Fecha'],
        loading: true,
        newBudget: new_budget,
        searchQuery: '',
        selectedBudget: {},
        selectedTask: {},
        selectedClient: "",
        selectedStatus: "",
        statusList: [],
        taskList: [],
        modelTasks: Object,
        isShowDateTasks: false,
        progress: 0,
        count: 0,
        countTotal: 0,
      },
      mounted: function() {
        this.getBudget();
        this.getTaskList();
      },
      updated: function () {
        this.$nextTick(function () {
          // Code that will run only after the
          // entire view has been re-rendered
          this.calculateTotals();
        })
      },
      methods: {
        getIcon: function(code){
          return status_budget[code].icon
        },
        getColor: function(code){
          if (status_budget[code]){
            return status_budget[code].color
          }
          return
        },
        calculateTotals: function(){
          var padres = $(".parent");
          $(".parent").each(function () {
              var sum = 0;
              $(".subtotal", this).each(function () {
                  var val = $.trim($(this).text());
                  if (val) {
                      val = Number(val.replace(/[^0-9\.-]+/g,""));
                      sum += !isNaN(val) ? val : 0;
                  }
              });
              $(this).find('.total').html(numeral(sum).format('0,0.00'));
          });
        },
        showEditAPUTask: function(model){
          this.currentTask = model;
          $("#editAPUTaskModal").modal('show');
        },
        getTaskList: function() {
          this.loading = true;
          this.$http.get(`/budget/api/budgets/${budget_id}/tasks`)
              .then((response) => {
                this.taskList = response.data;
                this.loading = false;
                this.modelTasks = {
                  name: "Titulo",
                  get_children: this.taskList,
                  unit: "Unidad",
                  quantity: "Cantidad",
                  projected_start_date: "F.Inicio",
                  projected_finish_date: "F.Fin",
                  subtotal: "Subtotal",
                };
                vm.progress = 0;
              })
              .catch((err) => {
                this.loading = false;
                console.log(":::getTaskList:::", err);
              })
        },
        getTask: function(model) {
          this.loading = true;
          // console.log("model: ", model);
          id = model.id;
          this.$http.get(`/budget/api/tasks/${id}/`)
              .then((response) => {
                this.currentTask = model
                this.selectedTask = response.data;
                // this.selectedClient = this.clientList.find(item => item.id === this.selectedBudget.client);
                $("#editTaskModal").modal('show');
                $("#name").focus();

                this.loading = false;
              })
              .catch((err) => {
                this.loading = false;
                console.log(err);
              })
        },
        updateTask: function() {
          this.loading = true;
          this.$http.put(`/budget/api/tasks/${this.selectedTask.id}/`, this.selectedTask)
              .then((response) => {
                this.loading = false;
                // this.selectedTask = response.data;
                this.currentTask.name = response.data.name;
                this.currentTask.unit = response.data.unit;
                this.currentTask.quantity = response.data.quantity;
                this.currentTask.projected_finish_date = response.data.projected_finish_date;
                this.currentTask.projected_start_date = response.data.projected_start_date;
                this.currentTask.price = response.data.price;
                $("#editTaskModal").modal('hide');
                this.errors = [];
                // this.getTaskList();
              })
              .catch((err) => {
                this.loading = false;
                this.errors = [],
                this.errors.push(err.body);
                console.log("error>>>", err);
              })
        },
        getBudget: function() {
          this.loading = true;
          this.$http.get(`/budget/api/budgets/${budget_id}/`)
              .then((response) => {
                this.selectedBudget = response.data;
                //this.selectedClient = this.clientList.find(item => item.id === this.selectedBudget.client);
                //$("#editModelModal").modal('show');
                //$("#title").focus();
                this.loading = false;
              })
              .catch((err) => {
                this.loading = false;
                console.log(":::::::", err);
              })
        },
        showFormImportTasksXML: function() {
          $("#formImportXMLModal").modal('show');
        },
        addTaskFromImport: function(){
          this.loading = true;
          this.$http.post(`/budget/api/tasks/`, this.currentTask)
            .then((response) => {
              vm.count = vm.count + 1;
              vm.progress = (vm.count * 100 / vm.count_total).toFixed(2);
              // this.loading = false;
            })
            .catch((err) => {
              this.loading = false;
              console.log(":::addBashTask_error:::", err, this.currentTask);
            })
        },
        updateTaskOrAddFromImport: function(){
          console.log("Falta desarrollar");
        },
        importTasksXML: function(e) {
          this.loading = true;
          $("#formImportXMLModal").modal('hide');
          // Cargar el archivo
          var $i = $('#fileXML'), // Put file input ID here
                   input = $i[0]; // Getting the element from jQuery

          var action_selected = document.querySelector('input[name="actionImport"]:checked').value;
          var tasks = [];
          console.log("Entro al boton importar");
          fr.onload = function () {
            var xmlDoc = $.parseXML( fr.result );
            console.log("fr.onload");
            vm.count_total = $(xmlDoc).find("Tasks").children('task').length;
            $(xmlDoc).find("Tasks").children('task').each(function(){
              current_task = {
                "budget": budget_id,
                "wbs": $(this).children('wbs').text(),
                "name": $(this).children('name').text() || "-",
                "projected_start_date": moment($(this).children('start').text()).format("YYYY-MM-DD"),
                "projected_finish_date": moment($(this).children('finish').text()).format("YYYY-MM-DD"),
                "position": $(this).children('id').text(),
                
              };
              vm.currentTask=current_task;
              vm.taskList.push(current_task);
              if (action_selected == "delete") {
                vm.addTaskFromImport();
              } else {
                vm.updateTaskOrAddFromImport();
              }
              
              
            });
            vm.getTaskList();
            console.log("Se importó...!!");
          };
          if ( input.files && input.files[0] ) {
            file = input.files[0]; // The file
            console.log("vm.taskList.length", vm.taskList.length);
            if (vm.taskList.length > 0 ){
              if (action_selected == "delete") {
                // Consulta si hace el borrado de todas las tareas y procede con la imprtación
                vm.willDeleteAllTasksAndImport();
              }
            } else {
              fr.readAsText( file );
            }
          } else {
            // Handle errors here
            vm.loading = false;
            alert( "File not selected or browser incompatible." )
          }
        },
        showDateTasks: function(){
          this.isShowDateTasks = !this.isShowDateTasks;
          return this.isShowDateTasks
        },
        willDeleteAllTasksAndImport: function() {
          swal({
            title: "¿Está seguro de borrar las tareas antes de importar?",
            text: "Todas las tareas de " + vm.selectedBudget.title + ", será borrado.",
            icon: "warning",
            buttons: ["Cancelar", "Borrar"],
            // button: "Borrar",
            dangerMode: true,
          })
          .then((willDelete) => {
            if (willDelete) {
              vm.loading = true;
              vm.$http.get(`/budget/api/budgets/${budget_id}/tasks/delete`)
                .then((response) => {
                  vm.taskList = [];
                  fr.readAsText( file );
                  vm.loading = false;
                })
                .catch((err) => {
                  vm.loading = false;
                  console.log(err);
                });
            };
          });
        },
      },
    },
  )

// $(document).on('click', '.dropdown-item', function(event) {
//   event.preventDefault();
//   $(this).toggleClass('dropdown-item-checked');

// });

