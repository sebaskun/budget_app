<template>
  <div>
    <b-form>
        <div>
          <div v-if="errors.length" class="alert alert-warning" role="alert">
              <b>Por favor corrija los siguientes errores:</b>
              <ul>
                <li v-for="error in errors">
                  <ul>
                    <li v-for="[key, value] in Object.entries(error)">
                      {{key}}: {{value[0]}}
                    </li>
                  </ul>
                </li>
              </ul>
          </div>
          <b-row>
            <b-col lg="4">
              <b-form-group id="code_group"
                label="Código:"
                label-for="code"
                description="Escriba el código">
                <b-form-input
                  id="code"
                  type="text"
                  v-model="form.code"
                  placeholder="Código">
                </b-form-input>
              </b-form-group>
            </b-col>
            <b-col lg="8">
              <b-form-group id="name_group"
                label="Nombre:"
                label-for="name">
                <b-form-input
                  id="name"
                  type="text"
                  v-model="form.name"
                  placeholder="Nombre">
                </b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-form-group id="description_group"
                label="Descripción:"
                label-for="description"
                description="Escriba una descripción para este recurso.">
                <b-form-textarea id="description"
                                 v-model="form.description"
                                 placeholder="Descripción del recurso"
                                 :rows="3"
                                 :max-rows="5">
                </b-form-textarea>
          </b-form-group>
          <b-row>
            <b-col lg="4">
              <b-form-group id="unit_group"
                label="Unidad:"
                label-for="unit"
                description="Escriba la unidad de costeo">
                <b-form-input
                  id="unit"
                  type="text"
                  v-model="form.unit"
                  placeholder="Unidad">
                </b-form-input>
              </b-form-group>
            </b-col>
            <b-col lg="4">
              <b-form-group id="currency_group"
                label="Moneda:"
                label-for="currency">
                <b-form-select
                  id="currency"
                  v-model="form.currency">
                  <option value="D">Dólares</option>
                  <option value="S">Soles</option>
                </b-form-select>
              </b-form-group>
            </b-col>
            <b-col lg="4">
              <b-form-group id="cost_group"
                label="Costo unitario:"
                label-for="cost"
                description="Escriba el costo del recurso">
                <b-form-input
                  id="cost"
                  type="number"
                  step=".1"
                  v-model="form.cost"
                  placeholder="Costo">
                </b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col lg="4">
              <b-form-group id="type_material_group"
                label="Tipo de costo:"
                label-for="type_cost">
                <b-form-select
                  id="type_cost"
                  v-model="form.type_material">
                  <option value="M">Médico</option>
                  <option value="W">Taller</option>
                  <option value="O">Operativo</option>
                  <option value="V">Varios</option>
                </b-form-select>
              </b-form-group>
            </b-col>
          </b-row>
          <b-button type="submit" @click.prevent="onSubmit" variant="primary">{{str_action}}</b-button>
          <b-button type="cancel" @click.prevent="onCancel" variant="danger">Cancelar</b-button>
        </div>
      </b-form>
  </div>
</template>

<script>
const config = {
    headers: {
      'content-type': 'multipart/form-data'
    }
  }
const url_api = "/resource/api/overhead/"

export default {
    props: ['action', 'id'],
    data() {
        return {
            errors: [],
            form: {
                code: "",
                name: "",
                description: "",
                unit: "Un",
                currency: "D",
                cost: "",
                type_cost: "V"
            },
            show: true,
            str_action: "Crear"
        }
    },
    mounted() {
      if (this.action == 'edit'){
        this.getItem()
        this.str_action = "Modificar"
      }
    },
    methods: {
      getItem() {
        let url = url_api + `${this.id}/`
        this.$http.get(url)
              .then((response) => {
                this.form = response.data
              })
              .catch((err) => {
                console.log(err);
              })
      },
      addItem() {
        const formData = new FormData()
        for ( var key in this.form ) {
          formData.append(key, this.form[key])
        }
        let url = url_api
        this.$http.post(url, formData, config)
          .then((response) => {
            this.$emit('itemAdded')
          })
          .catch((err) => {
            this.errors = []
            this.errors.push(err.body)
            console.log("error>>>", err)
          })
      },
      updateItem() {
        const formData = new FormData()
        for ( var key in this.form ) {
          formData.append(key, this.form[key])
        }
        let url = url_api + `${this.form.id}/`
        this.$http.put(url, formData, config)
          .then((response) => {
            this.$emit('itemAdded')
          })
          .catch((err) => {
            this.errors = []
            this.errors.push(err.body)
            console.log("error>>>", err)
          })
      },
      onSubmit (evt) {
        evt.preventDefault()
        if (this.action == 'edit'){
          this.updateItem()
        }else{
          this.addItem()
        }
      },
      onCancel (evt) {
        evt.preventDefault()
        /* Reset our form values */
        this.form.code = ""
        this.form.description =  ""
        this.form.unit =  ""
        this.form.currency = "D"
        this.form.cost = ""
        this.$emit('canceled')
      },
      // onChangePicture () {
      //   if (this.$refs.pictureInput.file){
      //     this.form.logo = this.$refs.pictureInput.file
      //   }
      // },
    }
}
</script>

