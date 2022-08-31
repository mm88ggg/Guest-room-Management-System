<template>
  <v-app>
    <v-card-title>
      <span class="headline">历史订单</span>
    </v-card-title>
    <v-card v-for="(order, n) in orders" :key="n" style="margin: 5px">
      <v-card-text>
        <v-simple-table>
          <template v-slot:default>
            <thead>
            <tr>
              <th class="text-left">
                项目
              </th>
              <th class="text-left">
                值
              </th>
            </tr>
            </thead>
            <tbody>
            <tr>
              <td>房间号</td>
              <td>{{ order.roomid }}</td>
            </tr>
            <tr>
              <td>下单时间</td>
              <td> {{ order.bookdate }}</td>
            </tr>
            <tr>
              <td>入住时间</td>
              <td>{{ order.fromdate }}</td>
            </tr>
            <tr>
              <td>退房时间</td>
              <td>{{ order.todate }}</td>
            </tr>
            <tr>
              <td>总价格</td>
              <td>{{ order.money }}</td>
            </tr>
            <tr>
              <td>是否有效</td>
              <td>{{ order.isActive }}</td>
            </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancelOrder(order)" :disabled="order.isActive === '否'">
          取消订单
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-app>
</template>

<script>
export default {
  name: "SearchOrderFunction",
  data() {
    return {
      orders: [],
    }
  },

  methods: {
    cancelOrder(item) {
      this.axios.post('/api/cancel_booking', {
        roomid: item.roomid,
        bookdate: this.changeDateFormat(item.bookdate),
        username: sessionStorage.getItem('username')
      }).then(res => {
        if (res.data.code === 0) {
          alert(res.data.msg)
          this.axios.post('/api/get_user_booking', {
            username: sessionStorage.getItem('username')
          }).then(response => {
            if (response.data.code === 0) {
              this.orders = response.data.data;
            } else {
              alert('获取订单失败');
            }
          });
        }
      });
    },

    changeDateFormat(date) {
      date = new Date(date)
      return date.toISOString().substr(0, 10) + ' ' + date.toISOString().substr(11, 8)
    },
  },

  created() {
    this.axios.post('/api/get_user_booking', {
      username: sessionStorage.getItem('username')
    }).then(response => {
      if (response.data.code === 0) {
        this.orders = response.data.data;
      } else {
        alert('获取订单失败');
      }
    });
  }
}
</script>

<style scoped>

</style>