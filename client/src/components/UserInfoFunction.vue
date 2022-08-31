<template>
  <div>
    <v-app-bar elevate-on-scroll color="white">
      <v-btn fab small color="white" style="margin-top: 10px" @click="backToProfile">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>

      <v-spacer></v-spacer>
    </v-app-bar>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-card-text>
              <v-form ref="form" lazy-validation>
                <v-text-field
                    v-model="username"
                    name="login"
                    label="用户名"
                    type="text"
                    readonly
                ></v-text-field>
                <v-text-field
                    v-model="id"
                    name="identity"
                    label="身份证"
                    type="text"
                    readonly
                ></v-text-field>
                <v-text-field
                    v-model="phone"
                    name="phone"
                    label="手机号"
                    type="text"
                    readonly
                ></v-text-field>
              </v-form>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>

export default {
  name: "UserInfoFunction",

  data() {
    return {
      username: "",
      id: "",
      phone: "",
    }
  },

  methods: {
    backToProfile() {
      this.$router.push("/profile");
    },
  },

  created() {
    this.axios.post('/api/get_user_info', {
      username: sessionStorage.getItem('username')
    }).then(res => {
      this.username = res.data.data.username
      this.id = res.data.data.id
      this.phone = res.data.data.tele
    })
  }
}
</script>

<style scoped>

</style>