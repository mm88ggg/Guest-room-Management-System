<template>
  <div>
    <br><br><br>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>忘记密码</v-toolbar-title>
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
                    label="请输入密码"
                    type="password"
                    v-model="password"
                    :rules="passwordRules"
                ></v-text-field>
                <v-text-field
                    id="password"
                    name="password"
                    label="请再次输入密码"
                    type="password"
                    v-model="passwordAgain"
                    :rules="passwordAgainRules"
                >
                </v-text-field>
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
              <v-btn color="secondary" @click="change" style="margin-left: 1em; margin-top: -10px" :disabled="!valid">确认修改</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>


  </div>
</template>

<script>
export default {
  name: "ForgetPwdView",
  data() {
    return {
      valid: true,

      canSend: true,

      count_time: 60,
      display: '发送验证码',
      validationcode: '',

      email: '',
      password: '',
      passwordAgain: '',

      emailRules: [
        (v) => !!v || '请输入邮箱',
        (v) => /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(v) || '请输入正确的邮箱',
      ],
      passwordRules: [
        (v) => !!v || '请输入密码',
        (v) => v.length >= 6 || '密码长度不能小于6位',
      ],
      passwordAgainRules: [
        (v) => !!v || '请再次输入密码',
        (v) => v === this.password || '两次密码不一致',
      ],
      validationcodeRules: [
        (v) => !!v || '验证码不能为空',
        (v) => v.length === 6 || '验证码长度不正确'
      ],
    }
  },

  methods: {
    send() {

    },

    change() {

    }
  }
}
</script>

<style scoped>

</style>