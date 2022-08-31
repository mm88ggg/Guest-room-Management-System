<template>
  <div>
    <br><br><br>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>修改密码</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field
                    v-model="email"
                    name="login"
                    label="请输入邮箱"
                    type="text"
                    :rules="emailRules"
                ></v-text-field>
                <v-text-field
                    id="password"
                    name="password"
                    label="请输入新密码"
                    type="password"
                    v-model="password"
                    :rules="passwordRules"
                ></v-text-field>
                <v-text-field
                    id="confirmpassword"
                    name="confirmpassword"
                    label="再次输入密码"
                    type="password"
                    v-model="confirmPassword"
                    :rules="confirmPasswordRules"
                ></v-text-field>
                <v-text-field
                    id="validationcode"
                    name="validationcode"
                    label="请输入验证码"
                    type="text"
                    v-model="validationcode"
                    :rules="validationcodeRules"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-btn color="secondary" @click="changePassword" style="margin-left: 1em; margin-top: -10px"
                     :disabled="!valid">修改密码
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn text :disabled="!canSend" @click="send">{{display}}</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "ChangePasswordView",
  data() {
    return {
      valid: true,
      canSend: true,

      count_time: 60,
      display: '发送验证码',

      email: '',
      password: '',
      confirmPassword: '',
      validationcode: '',
      emailRules: [
        (v) => !!v || '请输入邮箱',
        (v) => /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(v) || '请输入正确的邮箱',
      ],
      passwordRules: [
        (v) => !!v || '密码不能为空',
        (v) => v.length >= 6 || '密码长度不能小于6位'
      ],
      confirmPasswordRules: [
        (value) => !!value || '请再次输入密码',
        (value) => value === this.password || '两次输入的密码不一致'
      ],
      validationcodeRules: [
        (v) => !!v || '验证码不能为空',
        (v) => v.length === 6 || '验证码长度不正确'
      ],
    }
  },

  methods: {
    changePassword() {
      this.axios.post('/api/validate_code', {
        username: this.email,
        code: this.validationcode,
      }).then(response => {
        if (response.data.code === 0) {
          this.axios.post('/api/change_password', {
            username: this.email,
            password: this.password,
          }).then(response => {
            if (response.data.code === 0) {
              alert('修改成功，请重新登录');
              this.$router.push('/login')
            } else {
              console.log(response.data.message)
            }
          }).catch(error => {
            console.log(error.response.data.message)
          })
        } else {
          console.log(response.data)
        }
      }).catch(error => {
        console.log(error.response.data.message)
      })
    },

    send() {
      if (this.canSend) {
        this.canSend = false

        this.count_time = 60

        if (this.email === '') {
          alert('请输入邮箱')
          this.canSend = true
          return
        }

        this.axios.post('/api/send_code', {
          username: this.email,
          change: true
        }).then(res => {
          if (res.data.code === 0) {
            alert('验证码已发送，请注意查收')
          } else {
            alert('验证码发送失败')
          }
        })

        this.count_time_interval = setInterval(() => {
          this.display = '还剩下' + this.count_time + '秒'
          this.count_time--
          if (this.count_time === 0) {
            clearInterval(this.count_time_interval)
            this.canSend = true
            this.display = '发送验证码'
          }
        }, 1000)

      }
    },
  }
}
</script>

<style scoped>

</style>