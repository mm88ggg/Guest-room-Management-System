<template>
  <div>
    <v-card class="mx-auto" max-width="434" tile>

      <v-list two-line>
        <v-list-item-group
            active-class="green--text"
        >
          <template v-for="(item, index) in items">
            <v-list-item :key="item.title" @click="handleClick(index)">
              <template>
                <v-list-item-content>
                  <v-list-item-title>{{item.title}}</v-list-item-title>

                  <v-list-item-subtitle > {{ item.subtitle }}</v-list-item-subtitle>
                </v-list-item-content>
              </template>
            </v-list-item>

            <v-divider
                v-if="index < items.length - 1"
                :key="index"
            ></v-divider>
          </template>
        </v-list-item-group>
      </v-list>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "ProfileFunction",
  data() {
    return {
      username: sessionStorage.getItem('username'),

      items: [
        {
          subtitle: '查看身份证号、手机号等信息',
          title: '查看个人资料',
        },
        {
          subtitle: `可以查看历史订单，消费记录等`,
          title: '查看历史订单',
        },
        {
          subtitle: '可以使用旧密码修改密码',
          title: '修改密码',
        },
      ],
    }
  },

  methods: {
    handleClick(index) {
      if (index === 0) {
        this.$router.push('/userinfo');
      } else if (index === 1) {
        this.$router.push('/searchorder');
      } else if (index === 2) {
        this.$router.push('/change-password');
      }
    },
  },

  created() {
    this.$parent.app_bar_title = '个人中心';
  }
}
</script>

<style scoped>

</style>