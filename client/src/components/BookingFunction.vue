<template>
  <v-app style="background-color: whitesmoke">
    <div>
      <v-sheet outlined color="orange" rounded>
        <v-card class="d-flex flex-no-wrap justify-space-between" color="white" style="margin: 10px;">
          <v-container>
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
            </v-row>
            <v-card-actions>
              <v-btn @click="search" elevation="3" color="primary">
                查找可用房间
              </v-btn>
            </v-card-actions>
          </v-container>
        </v-card>

      </v-sheet>

      <v-col
          v-for="(item, i) in items"
          :key="i"
          cols="12"
          v-show="isShow"
      >
        <v-card
            elevation="0"
            shaped
        >
          <div :class="item.haveImg ? 'd-flex flex-no-wrap justify-space-between': ''">
            <div>
              <v-card-title
                  class="text-h5"
              >{{item.title}}</v-card-title>

              <v-card-subtitle >{{item.artist}}</v-card-subtitle>

              <v-card-actions>
                <v-btn elevation="0" rounded :disabled="!item.isAvailiable" @click="booking(item)">
                  {{ item.btnTxt }}
                </v-btn>
              </v-card-actions>
            </div>

            <v-avatar
                class="ma-3"
                size="125"
                tile
                v-if="item.haveImg"
            >
              <v-img :src="item.src"></v-img>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </div>
  </v-app>
</template>

<script>

export default {
  name: "BookingFunction",
  data() {
    return {
      roominfo: [],

      dates: [(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10), (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)],
      menu: false,
      modal: false,
      menu2: false,

      isShow: false,

      items: [],
    }
  },
  computed: {
    dateRangeText() {
      return this.dates.join(' ～ ');
    },
  },
  methods: {
    search() {
      this.isShow = false;

      this.axios.post('/api/get_availiable_room_type', {
        check_in_date: this.dates[0],
        check_out_date: this.dates[1],
      }).then(resp => {
        if (resp.data.code === 0) {
          this.roominfo = resp.data.data

          this.items = this.roominfo.map(item => {
            return {
              title: item.roomtype,
              artist: item.number === 0 ? '无可预定房间' : '有空闲房间 ' + (Number(item.price)).toFixed(2) + '元/晚',
              src: this.axios.defaults.baseURL + item.img,
              isAvailiable: item.number !== 0,
              btnTxt: item.number !== 0 ? '预定' : '无法预订',
              haveImg: item.img !== '',
              price: item.price
            }
          })

          // for (let i = 0; i < this.roominfo.length; i++) {
          //   this.items.push({
          //     title: this.roominfo[i].roomtype,
          //     artist: this.roominfo[i].number === 0 ? '无可预定房间' : '有空闲房间',
          //     src: this.axios.defaults.baseURL + this.roominfo[i].img,
          //     isAvailiable: this.roominfo[i].number !== 0,
          //     btnTxt: this.roominfo[i].number !== 0 ? '预定' : '无法预订',
          //     haveImg: this.roominfo[i].img !== '',
          //   })
          // }

          console.log(this.items)

          this.isShow = true;
        } else {
          alert(resp.data.msg)
        }
      });
    },
    booking(item) {
      sessionStorage.setItem('booking_username', sessionStorage.getItem('username'))
      sessionStorage.setItem('roomtype', item.title)
      sessionStorage.setItem('check_in_date', this.dates[0])
      sessionStorage.setItem('check_out_date', this.dates[1])
      console.log(sessionStorage.getItem('check_in_date'))
      this.$router.push('/payment')
    }
  }
}
</script>

<style scoped>

</style>