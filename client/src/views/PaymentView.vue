<template>
  <v-container>
    <v-card>
      <v-card-title>
        确认付款
      </v-card-title>
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
            <td>房间类型</td>
            <td>{{ roomtype }}</td>
          </tr>
          <tr>
            <td>入住时间</td>
            <td>{{ check_in_time }}</td>
          </tr>
          <tr>
            <td>退房时间</td>
            <td>{{ check_out_time }}</td>
          </tr>
          <tr>
            <td>天数</td>
            <td>{{ day }}</td>
          </tr>
          <tr>
            <td>总价格</td>
            <td>{{ price }}</td>
          </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card-actions>
        <v-btn color="primary" @click="success">
          付款成功
        </v-btn>
        <v-btn color="secondary" @click="unsuccess">
          付款失败
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-snackbar
        v-model="snackbar"
    >
      {{ text }}

      <template v-slot:action="{ attrs }">
        <v-btn
            color="pink"
            text
            v-bind="attrs"
            @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  name: "PaymentView",
  data() {
    return {
      roomid: sessionStorage.getItem("roomid"),
      roomtype: sessionStorage.getItem('roomtype'),
      check_in_time: sessionStorage.getItem('check_in_date'),
      check_out_time: sessionStorage.getItem('check_out_date'),

      day: 0,
      price: 0,

      snackbar: false,
      text: '',
    }
  },

  created() {
    console.log(this.roomtype)
    this.axios.post('/api/get_day_money', {
        roomid: this.roomid,
        roomtype: this.roomtype,
        check_in_date: this.check_in_time,
        check_out_date: this.check_out_time,
    }).then(resp => {
      if (resp.data.code === 0) {
        this.day = resp.data.num;
        this.price = resp.data.price;
        this.roomtype = resp.data.roomtype
        console.log(resp.data.roomtype)
      }
    })
  },

  methods: {
    success() {
      this.axios.post('/api/add_booking', {
        username: sessionStorage.getItem('booking_username'),
        roomid: this.roomid,
        roomtype: this.roomtype,
        fromdate: this.check_in_time,
        todate: this.check_out_time,
        isActive: '是'
      }).then(resp => {
        if (resp.data.code === 0) {
          this.snackbar = true
          this.text = '恭喜您，付款成功。即将返回上一个页面。'
          setTimeout(() => {
            this.$router.go(-1)
          }, 2000)
        } else {
          this.unsuccess()
        }
      })
    },

    unsuccess() {
      this.snackbar = true
      this.text = '抱歉，付款失败。可再次尝试付款'
    },
  }
}
</script>

<style scoped>

</style>