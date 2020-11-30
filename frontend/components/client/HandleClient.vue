<template>
    <div>
        <b-form>
            <div>
              <div v-if="errors.length" class="alert alert-warning" role="alert">
                  <b>Por favor corrija los siguientes errores:</b>
                  <ul>
                    <li v-for="error in errors" :key="error">
                      <ul>
                        <li v-for="[key, value] in Object.entries(error)" :key="key">
                          {{key}}: {{value[0]}}
                        </li>
                      </ul>
                    </li>
                  </ul>
              </div>
              <b-form-group id="name_group"
                    label="Nombre:"
                    label-for="name"
                    description="Nombre completo del cliente.">
                <b-form-input id="name"
                      type="text"
                      max-length=150
                      v-model="form.name"
                      placeholder="Ingresar nombre del cliente">
                </b-form-input>
              </b-form-group>
              <b-form-group id="short_name_group"
                    label="Nombre corto:"
                    label-for="short_name"
                    description="Nombre corto del cliente.">
                <b-form-input id="short_name"
                      type="text"
                      max-length=40
                      v-model="form.short_name"
                      placeholder="Ingresar un nombre corto del cliente">
                </b-form-input>
              </b-form-group>
              <b-form-group id="initials_group"
                    label="Iniciales:"
                    label-for="initials"
                    description="Iniciales del cliente.">
                <b-form-input id="initials"
                      type="text"
                      max-length=3
                      v-model="form.initials"
                      placeholder="Ingresar las iniciales del cliente">
                </b-form-input>
              </b-form-group>
              <b-form-group id="logo_group"
                    label="Logo:"
                    description="Seleccione un archivo o arrastre una imagen.">
                <picture-input
                  ref="pictureInput"
                  :prefill="form.logo"
                  @change="onChangePicture"
                  width="200"
                  height="200"
                  margin="16"
                  accept="image/jpeg,image/png"
                  size="10"
                  :customStrings="{
                    upload: '<h1>Bummer!</h1>',
                    drag: 'Arrastre una imagen aquí',
                    change: 'Cambiar imagen'
                  }">
                </picture-input>
              </b-form-group>

                <b-button type="submit" @click.prevent="onSubmit" variant="primary">{{ str_action }}</b-button>
                <b-button type="cancel" @click.prevent="onCancel" variant="danger">Cancelar</b-button>

            </div>
        </b-form>
    </div>
</template>

<script>

import PictureInput from 'vue-picture-input'

const config = {
    headers: {
      'content-type': 'multipart/form-data'
    }
  }

export default {
    components: {
      PictureInput
    },
    props: ['action', 'id'],
    data() {
        return {
            errors: [],
            form: {
              id: "",
              name: "",
              short_name: "",
              initials: "",
              logo: "",
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
        let url = `/client/api/clients/${this.id}/`
        this.$http.get(url)
              .then((response) => {
                this.form = response.data
                let url = this.form.logo
                // let name = url.split('/').pop()
                // console.log("url:", url, "name:", name )
                // this.form.logo = new File([url], name, {type: "image/jpeg,image/png",})
                // this.$refs.pictureInput.prefill = this.form.logo
                // this.$refs.pictureInput.preloadImage(this.form.logo)
                // this.form.logo = this.$refs.pictureInput.file
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
        let url = '/client/api/clients/'
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
        let url = `/client/api/clients/${this.form.id}/`
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
        this.form.name = ""
        this.form.short_name =  ""
        this.form.initials =  ""
        this.form.logo = ""
        this.$emit('canceled')
      },
      onChangePicture () {
        if (this.$refs.pictureInput.file){
          this.form.logo = this.$refs.pictureInput.file
        }
      },
    }
}
</script>
