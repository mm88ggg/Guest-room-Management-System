<template>
  <v-main>
    <div style="margin: 20px">
      <v-card flat>

        <v-card-title>选择入住与退房时间</v-card-title>
        <v-row>
          <v-col>
            <v-dialog
                ref="dialog"
                v-model="modal"
                :return-value.sync="dates"
                persistent
                width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                    v-model="dateRangeText"
                    label="点击选取时间"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                >{{ dates }}
                </v-text-field>
              </template>
              <v-date-picker
                  v-model="dates"
                  range
              >
                <v-spacer></v-spacer>
                <v-btn
                    text
                    color="primary"
                    @click="modal = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                    text
                    color="primary"
                    @click="$refs.dialog.save(dates)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-dialog>
          </v-col>
          <v-col>
            <v-btn @click="search" elevation="3" color="primary">
              查找可用房间
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </div>

    <v-divider></v-divider>

    <v-card flat v-show="show_room">
      <v-card-title>可预定房间列表</v-card-title>
      <v-data-table
          :headers="headers"
          :items="this.roominfo"
          :search="search_roomid"
          class="elevation-1">
        <template v-slot:top>
          <v-text-field
              v-model="search_roomid"
              label="查询关键字"
              class="mx-4"
          ></v-text-field>
        </template>
      </v-data-table>
    </v-card>

    <v-container v-show="show_room">
      <v-row>
        <v-col>
          <v-text-field
              v-model="booking_username"
              label="请输入要预定用户的用户名"
              type="text"
          >
          </v-text-field>
        </v-col>
        <v-col>
          <v-text-field
              v-model="room_id"
              label="请输入房间号"
              type="text"
          >
          </v-text-field>
        </v-col>
        <v-col>
          <v-btn @click="booking" color="primary" style="margin-top: 10px">
            预定
          </v-btn>
        </v-col>
      </v-row>
    </v-container>

    <v-divider></v-divider>

    <v-card-title>
      订单信息
    </v-card-title>

    <v-card flat style="margin: 40px">
      <v-row>
        <v-col>
          <v-text-field
              v-model="username"
              name="login"
              label="请输入用户名"
              type="text"
          ></v-text-field>
        </v-col>
        <v-col>
          <v-btn style="margin-top: 10px" color="primary" @click="getUserBooking">
            搜索
          </v-btn>
          <v-btn @click="updateBooking" style="margin-top: 10px">
            刷新数据
          </v-btn>
        </v-col>
        <v-col>
          <v-text-field
              v-model="money"
              name="login"
              label="请输入要扣款的金额"
              type="number"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-card>


    <v-simple-table>
      <template v-slot:default>
        <thead>
        <tr>
          <th class="text-left">
            用户
          </th>
          <th class="text-left">
            房间号
          </th>
          <th class="text-left">
            下单时间
          </th>
          <th class="text-left">
            入住时间
          </th>
          <th class="text-left">
            退房时间
          </th>
          <th class="text-left">
            总价
          </th>
          <th class="text-left">
            是否为有效订单
          </th>
          <th class="text-left">
            操作
          </th>
        </tr>
        </thead>
        <tbody>
        <tr
            v-for="item in desserts"
            :key="item.name"
        >
          <td>{{ item.username }}</td>
          <td>{{ item.roomid }}</td>
          <td>{{ item.bookdate }}</td>
          <td>{{ item.fromdate }}</td>
          <td>{{ item.todate }}</td>
          <td>{{ item.money }}</td>
          <td>{{ item.isActive }}</td>
          <td>
            <v-icon
                small
                class="mr-2"
                @click="checkIn(item)"
                :disabled="!(item.isActive === '是')"
            >
              入住
            </v-icon>
            <v-icon
                small
                @click="checkOut(item)"
                :disabled="!(item.isActive === '是')"
            >
              退房
            </v-icon>
          </td>
        </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-main>
</template>

<script>
export default {
  name: "BookingManagement",
  data() {
    return {
      search_roomid: '',
      headers: [
        {text: '房间号', value: 'roomid'},
        {text: '房间状态', value: 'roomstate'},
        {text: '房间类型', value: 'roomtype'},
        {text: '备注', value: 'note'},
      ],
      roominfo: [],
      show_room: false,
      room_id: '',
      booking_username: '',

      desserts: [],
      username: '',
      money: 0.0,

      dates: [(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10), (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)],
      menu: false,
      modal: false,
      menu2: false,
    }
  },

  beforeCreate() {
    this.axios.get('/api/get_booking').then(resp => {
      if (resp.data.code === 0) {
        this.desserts = resp.data.data
      }
    })
  },

  methods: {
    getUserBooking() {
      this.axios.post('/api/get_user_booking', {
        username: this.username,
      }).then(resp => {
        if (resp.data.code === 0) {
          this.desserts = resp.data.data
        }
      })
    },

    updateBooking() {
      this.axios.get('/api/get_booking').then(resp => {
        if (resp.data.code === 0) {
          this.desserts = resp.data.data
        }
      })
    },

    changeDateFormat(date) {
      date = new Date(date)
      return date.toISOString().substr(0, 10) + ' ' + date.toISOString().substr(11, 8)
    },

    checkIn(item) {
      this.axios.post('/api/check_in', {
        username: item.username,
        roomid: item.roomid,
        bookdate: this.changeDateFormat(item.bookdate),
      }).then(resp => {
        if (resp.data.code === 0) {
          alert('入住成功')
          this.updateBooking()
        } else {
          alert(resp.data.msg)
        }
      })
    },

    checkOut(item) {
      this.axios.post('/api/check_out', {
        username: item.username,
        roomid: item.roomid,
        bookdate: this.changeDateFormat(item.bookdate),
        money: this.money,
      }).then(resp => {
        if (resp.data.code === 0) {
          alert('退房成功')
          this.updateBooking()
        }
      })
    },

    search() {
      this.axios.post('/api/get_availiable_room', {
        check_in_date: this.dates[0],
        check_out_date: this.dates[1],
      }).then(resp => {
        if (resp.data.code === 0) {
          this.roominfo = resp.data.data
          this.show_room = true
          console.log(this.roominfo)
        }
      })
    },

    booking() {
      sessionStorage.setItem('booking_username', this.booking_username)
      sessionStorage.setItem('roomid', this.room_id)
      sessionStorage.setItem('check_in_date', this.dates[0])
      sessionStorage.setItem('check_out_date', this.dates[1])
      this.$router.push('/payment')
    },
  },
  computed: {
    dateRangeText() {
      return this.dates.join(' ～ ');
    },
  },
}
</script>

<style scoped>

</style>