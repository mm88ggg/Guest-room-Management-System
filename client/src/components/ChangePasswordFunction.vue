<template>
<!--change password use old password-->
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
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field
                    v-model="oldPassword"
                    name="oldPassword"
                    label="旧密码"
                    type="password"
                    :rules="oldPasswordRules"
                ></v-text-field>
                <v-text-field
                    v-model="newPassword"
                    name="newPassword"
                    label="新密码"
                    type="password"
                    :rules="newPasswordRules"
                ></v-text-field>
                <v-text-field
                    v-model="confirmPassword"
                    name="confirmPassword"
                    label="确认密码"
                    type="password"
                    :rules="confirmPasswordRules"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" :disabled="!valid" @click="change">确认修改</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "ChangePasswordFunction",
  data() {
    return {
      valid: true,
      username: sessionStorage.getItem('username'),
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',

      oldPasswordRules: [
        (v) => !!v || "旧密码不能为空",
        (v) => (v && v.length >= 6) || "旧密码长度不能小于6位",
        (v) => (v && v.length <= 20) || "旧密码长度不能大于20位",
      ],
      newPasswordRules: [
        (v) => !!v || "新密码不能为空",
        (v) => (v && v.length >= 6) || "新密码长度不能小于6位",
        (v) => (v && v.length <= 20) || "新密码长度不能大于20位",
      ],
      confirmPasswordRules: [
        (v) => !!v || "确认密码不能为空",
        (v) => (v && v.length >= 6) || "确认密码长度不能小于6位",
        (v) => (v && v.length <= 20) || "确认密码长度不能大于20位",
        (v) => v === this.newPassword || "两次密码不一致",
      ],
    }
  },

  methods: {
    backToProfile() {
      this.$router.push('/profile');
    },

    change() {
      this.axios.post('/api/change_password_by_old_password', {
        username: this.username,
        old_password: this.oldPassword,
        new_password: this.newPassword,
      }).then(res => {
        if (res.data.code === 0) {
          alert('修改成功，返回个人中心');
          this.$router.push('/profile');
        } else {
          console.log(res);
        }
      }).catch(err => {
        console.log(err);
      });
    }
  }
}
</script>

<style scoped>

</style>