<template>
  <div>
    <v-app-bar elevate-on-scroll color="white" flat>
      <v-btn fab small color="white" style="margin-top: 10px;" @click="backToLogin">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-stepper v-model="e1" style="max-width: 654px">
            <v-stepper-header>
              <v-stepper-step
                  :complete="e1 > 1"
                  step="1"
              >
                输入基本信息
              </v-stepper-step>

              <v-divider></v-divider>

              <v-stepper-step
                  :complete="e1 > 2"
                  step="2"
              >
                Name of step 2
              </v-stepper-step>

              <v-divider></v-divider>

              <v-stepper-step step="3">
                Name of step 3
              </v-stepper-step>
            </v-stepper-header>

            <v-stepper-items>
              <v-stepper-content step="1">

                <v-card>
                  <v-toolbar dark color="primary" flat>
                    <v-toolbar-title>输入基本信息</v-toolbar-title>
                  </v-toolbar>
                  <v-card-text>
                    <v-form ref="form" v-model="valid" lazy-validation>
                      <v-text-field
                          v-model="username"
                          name="login"
                          label="邮箱"
                          type="text"
                          :rules="nameRules"
                      ></v-text-field>
                      <v-text-field
                          id="password"
                          name="password"
                          label="密码"
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
                          :rules="confirmPasswordRules.concat(passwordConfirmationRule)"
                      ></v-text-field>
                      <v-text-field
                          v-model="id"
                          name="identity"
                          label="身份证"
                          type="text"
                          :rules="idRules"
                      ></v-text-field>
                      <v-text-field
                          v-model="phone"
                          name="phone"
                          label="手机号"
                          type="text"
                          :rules="phoneRules"
                      ></v-text-field>
                    </v-form>
                    <v-checkbox
                        v-model="checkbox"
                        :rules="[(v) => !!v || '请同意条款']"
                        label="同意(并不存在的)用户条款"
                        required
                        style="margin-top: -5px"
                    ></v-checkbox>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="secondary" @click="reset">重制</v-btn>
                    <v-btn color="secondary" @click="resetValidation">清除提示</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" :disabled="!valid" @click="register">注册</v-btn>
                  </v-card-actions>
                </v-card>

              </v-stepper-content>

              <v-stepper-content step="2">
                <v-card
                    elevation="0"
                    height="200px"
                >
                  <v-card-title>请输入邮箱验证码</v-card-title>
                  <v-card-text>
                    <v-form ref="form" v-model="valid2" lazy-validation>
                      <v-text-field
                          v-model="code"
                          name="code"
                          label="六位数验证码"
                          type="text"
                          :rules="codeRules"
                      ></v-text-field>
                    </v-form>
                  </v-card-text>

                  <v-card-actions>
                    <v-btn
                        color="primary"
                        @click="validateCode"
                        :disabled="!valid2"
                    >
                      继续
                    </v-btn>

                    <v-btn text @click="backToPrevious">
                      返回上一步
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-stepper-content>

              <v-stepper-content step="3">
                <v-card
                    flat
                    class="mb-12"
                    height="200px"
                >
                  <v-card-title style="font-size: 50px; margin: 20px;">恭喜您，注册成功🎉</v-card-title>

                </v-card>
                <v-btn
                    color="primary"
                    @click="backToLogin"
                >
                  完成注册，返回登录
                </v-btn>
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
        </v-flex>
      </v-layout>
    </v-container>


  </div>
</template>

<script>
export default {
  name: "RegisterView",
  data: () => ({
    valid: true,
    username: '',
    nameRules: [
      v => !!v || '请输入电子邮箱',
      v => /.+@.+\..+/.test(v) || '请输入有效的电子邮箱',
    ],
    password: '',
    confirmPassword: '',
    passwordRules: [
      (value) => !!value || '请输入密码',
      (value) => (value && value.length >= 6) || '密码请至少输入六位数',
    ],
    confirmPasswordRules: [
      (value) => !!value || '请再次输入密码',
    ],
    id: '',
    idRules: [
      (value) => !!value || '请输入身份证号',
      (value) => (value && value.length === 18) || '身份证号请输入18位',
      (v) => {
        const reg = /^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/;
        return reg.test(v) || '身份证号格式不正确';
      }
    ],
    phone: '',
    phoneRules: [
      (value) => !!value || '请输入手机号',
      (value) => (value && value.length === 11) || '请输入正确的手机号',
    ],
    checkbox: false,

    code: '',
    codeRules: [
      (value) => !!value || '请输入验证码',
      (value) => (value && value.length === 6) || '请输入正确的验证码',
    ],

    valid2: true,

    cnt: 0,
    e1: 1,
  }),

  methods: {
    validate() {
      this.$refs.form.validate()
    },
    reset() {
      this.$refs.form.reset()
    },
    resetValidation() {
      this.$refs.form.resetValidation()
    },

    backToLogin() {
      this.$router.push('/login')
    },

    register() {
      if (this.checkbox === false) {
        alert('请同意用户条款')
      } else {
        this.axios.post('/api/register', {
          username: this.username,
          password: this.password,
          id: this.id,
          phone: this.phone,
        }).then(response => {
          if (response.data.code === 0) {
            this.e1 = 2
            this.axios.post('/api/send_code', {
              username: this.username,
            }).then(res => {
              if (res.data.code === 0) {
                alert('验证码已发送，请注意查收')
              } else {
                alert('验证码发送失败')
              }
            })
          } else {
            alert(response.data.msg)
          }
        }).catch(error => {
          console.log(error)
        })
      }
    },
    validateCode() {
      this.axios.post('/api/validate_code', {
        username: this.username,
        code: this.code,
      }).then(res => {
        if (res.data.code === 0) {
          this.e1 = 3
        } else {
          alert(res.data.msg)
        }
      })
    },
    backToPrevious() {
      this.e1 -= 1
    },
  },

  computed: {
    passwordConfirmationRule() {
      return () =>
          this.password === this.confirmPassword || "两次密码不匹配";
    },
  },
}
</script>

<style scoped>

</style>