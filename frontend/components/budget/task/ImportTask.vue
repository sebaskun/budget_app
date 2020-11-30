<template>
    <div>
        <b-form>
          <b-form-group id="file_group"
              label="Archivo:"
              label-for="file"
              description="Selecciona un archivo de formato XML.">
              <b-form-file
                      id="file"
                      v-model="file"
                      :state="Boolean(file)"
                      placeholder="Selecciona un archivo..."
                      accept=".xml"></b-form-file>
          </b-form-group>
          <b-button type="submit" @click.prevent="onSubmit" variant="primary">Importar</b-button>
          <b-button type="button" @click.prevent="onCancel" variant="danger">Cancelar</b-button>
        </b-form>
    </div>
</template>

<script>
  import $ from 'jquery'
  import moment from 'moment'
  export default {
    props: ['id','otro'],
    data() {
      return {
        file: null,
        total_tasks: 0,
        count_tasks: 0,
      }
    },
    methods: {
      onSubmit(){
        if (Boolean(this.file)){
          let fr = new FileReader()
          let vm = this
          let tasks = []
          fr.onload = function() {
            let xmlDoc = $.parseXML( fr.result )
            // console.log("fr.onload");
            this.total_task = $(xmlDoc).find("Tasks").children('task').length;
            $(xmlDoc).find("Tasks").children('task').each(function(){
              let projected_start_date = moment($(this).children('start').text())
              let projected_finish_date = moment($(this).children('finish').text())
              let task = {
                budget: vm.id,
                wbs: $(this).children('wbs').text(),
                name: $(this).children('name').text() || "-",
                projected_start_date: (projected_start_date.isValid() ? projected_start_date.format("YYYY-MM-DD"): null),
                projected_finish_date: (projected_finish_date.isValid() ? projected_finish_date.format("YYYY-MM-DD"): null),
                position: $(this).children('id').text(),
                outline_level: parseInt($(this).children('outlinelevel').text()),
                uid: parseInt($(this).children('uid').text())
              }
              tasks.push(task)
              // console.log($(this))
            })
            // se envía todas las tareas al padre y se indica que se borre todas las tareas previas
            vm.$emit('tasksImported', tasks, true)
            // vm.$store.dispatch('requestTaskList', vm.id)
          }
          fr.readAsText(this.file)
        }
      },
      onCancel(){
        this.$emit('cancelImport')
      }
    }
  }
</script>
