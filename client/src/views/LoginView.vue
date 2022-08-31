<template>
  <div>
    <br><br><br>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>客房管理系统 -- 登录</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field
                    prepend-icon="mdi-account"
                    v-model="email"
                    name="login"
                    label="请输入邮箱"
                    type="text"
                    :rules="emailRules"
                ></v-text-field>
                <v-text-field
                    prepend-icon="mdi-lock"
                    id="password"
                    name="password"
                    label="请输入密码"
                    type="password"
                    v-model="password"
                    :rules="passwordRules"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-btn color="secondary" @click="login" style="margin-left: 1em; margin-top: -20px" :disabled="!valid">登录</v-btn>
              <v-btn @click="forget" outlined color="black" class="create" >忘记密码</v-btn>
            </v-card-actions>
            <v-divider></v-divider>
            <v-card-title>
              <h5>还没有账号？</h5>
            </v-card-title>
            <v-card-actions>
              <v-btn @click="create" outlined color="black" class="create" >注册账号</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>


  </div>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      email: '',
      password: '',
      emailRules: [
        (v) => !!v || '请输入邮箱',
      ],
      passwordRules: [
        (value) => !!value || '请输入密码'
      ],
      valid: false,
    }
  },
  methods: {
    login() {
      this.$refs.form.validate()
      if (this.valid) {
        this.axios.post('/api/login', {
          username: this.email,
          password: this.password
        }).then(resp => {
          if (resp.data.code === 0) {
            console.log(resp.data.user)
            sessionStorage.setItem('accessToken', resp.data.token)
            sessionStorage.setItem('username', resp.data.user)
            if (resp.data.type === 'staff') {
              this.$router.push('/manage/room')
            } else {
              this.$router.push('/booking')
            }
          } else {
            alert(resp.data.msg)
          }
        })
      }
    },
    create() {
      this.$router.push('/register')
    },
    forget() {
      this.$router.push('/change_pwd')
    },
  },
  validate() {
    this.$refs.form.validate()
  },
}
</script>

<style scoped>
.create {
  text-transform: capitalize;
  margin-top: -5px;
  margin-bottom: 1em;
  margin-left: 1em;
}


</style>