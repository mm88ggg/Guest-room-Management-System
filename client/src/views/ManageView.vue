<template>
  <v-app id="inspire">

    <v-navigation-drawer
        v-model="drawer"
        app
    >
      <v-sheet
          color="grey lighten-4"
          class="pa-4"
      >
        <v-avatar
            class="mb-4"
            color="primary"
            size="64"
            style="color: white; font-size: 30px"
        >{{ staffid }}</v-avatar>

        <div>欢迎您，{{ staffid }}号前台</div>
      </v-sheet>

      <v-divider></v-divider>

      <v-list>
        <v-list-item
            v-for="[icon, text] in links"
            :key="icon"
            link
            @click="menuActionClick(text)">

          <v-list-item-icon>
            <v-icon>{{ icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title> {{title}} </v-toolbar-title>

    </v-app-bar>

    <router-view></router-view>
  </v-app>
</template>

<script>
export default {
  name: 'ManageView',
  data: () => ({
    cards: ['Today', 'Yesterday'],
    drawer: null,
    links: [
      ['mdi-inbox-arrow-down', '客房管理'],
      ['mdi-account', '账户管理'],
      ['mdi-package', '订单管理'],
    ],

    title: '客房管理',

    staffid: sessionStorage.getItem('username'),
  }),

  methods: {
    menuActionClick(text) {
      switch (text) {
        case '客房管理':
          this.$router.push('/manage/room');
          break;
        case '账户管理':
          this.$router.push('/manage/user');
          break;
        case '订单管理':
          this.$router.push('/manage/booking');
          break;
      }
      this.title = text
    },
  }
}
</script>