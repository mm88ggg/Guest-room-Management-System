<template>
  <div>
    <v-navigation-drawer
        v-model="drawer"
        app
        right
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            欢迎, {{username}}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list
          dense
          nav
      >
        <v-list-item
            v-for="item in drawerItems"
            :key="item.title"
            link
            @click="menuActionClick(item)"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-card class="overflow-hidden">
      <v-app-bar
          absolute
          color="indigo darken-2"
          dark
          shrink-on-scroll
          prominent
          scroll-target="#scrolling-techniques"
      >

        <v-avatar
            color="teal"
            size="30"
            style="color: #fff; margin-top: 10px; font-size: 15px"
        >{{username[0]}}</v-avatar>

        <v-app-bar-title style="margin-left: 15px">{{app_bar_title}}</v-app-bar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>

        <v-btn icon>
          <v-icon>mdi-heart</v-icon>
        </v-btn>

        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </v-app-bar>
      <v-sheet
          id="scrolling-techniques"
          class="overflow-y-auto"
          max-height="844px"
      >
          <br><br><br><br><br><br>
          <router-view></router-view>
      </v-sheet>
    </v-card>


  </div>
</template>

<script>
export default {
  name: "MainView",

  data() {
    return {
      value: 1,
      username: sessionStorage.getItem('username'),
      drawer: false,
      drawerItems: [
        {
          icon: 'mdi-home',
          title: '首页',
          action: 'home',
        },
        {
          icon: 'mdi-account-circle',
          title: '个人中心',
          action: 'profile',
        },
        {
          icon: 'mdi-bell',
          title: '查看订单',
          action: 'order',
        },
        {
          icon: 'mdi-logout',
          title: '退出登录',
          action: 'logout',
        },
      ],

      app_bar_title: '酒店预订',
    }
  },

  methods: {
    logout() {
      sessionStorage.clear()
      this.$router.push('/login');
    },
    menuActionClick(item) {
      if (item.action === 'logout') {
        this.logout()
      } else if (item.action === 'profile' && this.$route.path !== '/profile') {
        this.$router.push('/profile')
        this.app_bar_title = '个人中心'
      } else if (item.action === 'home' && this.$route.path !== '/booking') {
        this.$router.push('/booking')
        this.app_bar_title = '酒店预订'
      } else if (item.action === 'order' && this.$route.path !== '/searchorder') {
        this.$router.push('/searchorder')
        this.app_bar_title = '查看订单'
      }
    },
  },

  computed: {},
}
</script>

<style scoped>

.v-item-group.v-bottom-navigation .v-btn.v-size--default {
  height: inherit;
}

</style>