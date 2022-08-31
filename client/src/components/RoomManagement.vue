<template>
  <v-main>
    <v-container class="py-8 px-6" fluid>
      <v-row style="background-color: #417598">

        <v-col style="color: white; font-size: 50px; margin: 20px">
          目前你选择的房间是：{{ selected_room }}
        </v-col>

        <v-col>
          <v-container>
            <v-row>
              <v-col
                  v-for="(roomState, n) in roomStates"
                  :key="n"
              >
                <v-card :color="roomState.color" :dark="roomState.color !== 'white'">
                  <v-card-title>
                    {{ roomState['statename'] }}
                  </v-card-title>

                  <v-card-subtitle>
                    一共有{{ roomState['number'] }}间房
                  </v-card-subtitle>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="1" v-for="(room, n) in roomList" :key="n">
          <v-btn :color="state_to_color[room['roomstate']]"
                 :dark="state_to_color[room['roomstate']] !== 'white'"
                 @click="selectRoom(room)"
          >
            <v-card-title>
              {{ room['roomid'] }}
            </v-card-title>
          </v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="6">
          <v-btn color="primary" @click="makeRoomBusy()" style="margin: 10px">
            将房间置为处理状态
          </v-btn>
          <v-btn color="primary" @click="makeRoomAva()" style="margin: 10px">
            将房间置为空闲状态
          </v-btn>
          <v-btn
              color="primary"
              @click="updateRoomInfo"
              style="margin: 10px"
          >
            Reset
          </v-btn>
        </v-col>
        <v-col>
          <v-file-input
              accept=".csv"
              label="房间信息表"
              ref="myfile"
              v-model="file"
          ></v-file-input>
        </v-col>
        <v-col>
          <v-btn @click="submitFiles">
            <v-icon>mdi-upload</v-icon>
            上传并修改
          </v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-divider></v-divider>
      </v-row>
      <br>
      <v-card>
        <v-card-title>
          房间详细列表
        </v-card-title>
        <template>
          <v-data-table
              :headers="headers"
              :items="desserts"
              sort-by="roomid"
              class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar
                  flat
              >
                <v-toolbar-title>房间信息</v-toolbar-title>
                <v-divider
                    class="mx-4"
                    inset
                    vertical
                ></v-divider>
                <v-spacer></v-spacer>
                <v-dialog
                    v-model="dialog"
                    max-width="500px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        color="primary"
                        dark
                        class="mb-2"
                        v-bind="attrs"
                        v-on="on"
                    >
                      添加房间
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="text-h5">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col
                              cols="12"
                              sm="6"
                              md="4"
                          >
                            <v-text-field
                                v-model="editedItem.roomid"
                                label="房间号(非必要不修改)"
                            ></v-text-field>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="6"
                              md="4"
                          >
                            <v-select
                                v-model="editedItem.roomtype"
                                label="房间类型"
                                :items="roomTypes"
                            ></v-select>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="6"
                              md="4"
                          >
                            <v-text-field
                                v-model="editedItem.roomstate"
                                label="房间状态"
                            ></v-text-field>
                          </v-col>
                          <v-col
                              cols="12"
                              sm="6"
                              md="4"
                          >
                            <v-text-field
                                v-model="editedItem.note"
                                label="备注"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                          color="blue darken-1"
                          text
                          @click="close"
                      >
                        Cancel
                      </v-btn>
                      <v-btn
                          color="blue darken-1"
                          text
                          @click="save"
                      >
                        Save
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <v-dialog v-model="dialogDelete" max-width="500px">
                  <v-card>
                    <v-card-title class="text-h5">确定删除此房间？</v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                      <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon
                  small
                  class="mr-2"
                  @click="editItem(item)"
              >
                mdi-pencil
              </v-icon>
              <v-icon
                  small
                  @click="deleteItem(item)"
              >
                mdi-delete
              </v-icon>
            </template>

          </v-data-table>
        </template>
      </v-card>
    </v-container>

  </v-main>
</template>

<script>
export default {
  name: "RoomManagement",
  data() {
    return {
      file: null,

      roomTypes: [],
      roomStates: [],
      roomList: [],
      roomStateNumber: {},
      state_to_color: {},
      selected_room: '',

      dialog: false,
      dialogDelete: false,
      headers: [
        {
          text: '房间号',
          align: 'start',
          sortable: true,
          value: 'roomid',
        },
        {text: '房间类型', value: 'roomtype'},
        {text: '房间状态', value: 'roomstate'},
        {text: '备注', value: 'note'},
        {text: '入住用户', value: 'username'},
        {text: '动作', value: 'actions', sortable: false},
      ],
      desserts: [],
      editedIndex: -1,
      editedItem: {
        roomid: '',
        roomtype: '',
        roomstate: '',
        note: '',
      },
      defaultItem: {
        roomid: '',
        roomtype: '',
        roomstate: '空闲',
        note: '',
      },
    }
  },
  methods: {
    submitFiles() {
      if (this.file) {
        let formData = new FormData();

        // files
        formData.append("files", this.file, this.file.name);

        this.axios
            .post("/api/upload_file", formData)
            .then(response => {
              if (response.data.code === 0) {
                console.log("Success!");
                console.log({ response });

                alert("上传成功");
                this.updateRoomInfo();
              }
            })
            .catch(error => {
              console.log({ error });
            });
      } else {
        console.log("there are no files.");
      }
    },

    initialize() {
      setTimeout(() => {
        this.desserts = this.roomList
      }, 500)
    },

    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem(item) {
      this.editedIndex = this.desserts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm() {
      this.desserts.splice(this.editedIndex, 1)
      this.axios.post('/api/delete_room', {
        'roomid': this.editedItem.roomid
      })
      setTimeout(() => {
        this.updateRoomInfo()
      }, 1000)
      this.closeDelete()
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save() {
      if (this.editedIndex > -1) {
        // edit
        this.axios.post('/api/edit_room', this.editedItem)
      } else {
        // add
        this.axios.post('/api/add_room', this.editedItem)
      }
      setTimeout(() => {
        this.updateRoomInfo()
      }, 500)
      this.close()
    },

    updateRoomInfo() {
      this.axios.get('api/get_room_state').then(res => {
        if (res.data.code === 0) {
          this.roomStates = res.data.data;
        }
      });
      this.axios.get('api/get_room_list').then(res => {
        if (res.data.code === 0) {
          this.roomList = res.data.data;

        }
      });
      setTimeout(() => {
        for (let i = 0; i < this.roomStates.length; i++) {
          this.roomStateNumber[this.roomStates[i]['statename']] = 0;
          this.state_to_color[this.roomStates[i]['statename']] = this.roomStates[i]['color'];
        }
        for (let i = 0; i < this.roomList.length; i++) {
          this.roomStateNumber[this.roomList[i]['roomstate']]++;
        }
        for (let i = 0; i < this.roomStates.length; i++) {
          this.roomStates[i]['number'] = this.roomStateNumber[this.roomStates[i]['statename']]
        }
        this.initialize()
      }, 300)
    },

    selectRoom(item) {
      this.selected_room = item.roomid;
    },

    makeRoomBusy() {
      if (this.selected_room === '') {
        alert('请选择房间');
      }

      this.axios.post('api/make_room_busy', {
        roomid: this.selected_room
      }).then(res => {
        if (res.data.code === 0) {
          this.updateRoomInfo();
        }
      });
    },

    makeRoomAva() {
      if (this.selected_room === '') {
        alert('请选择房间');
      }

      this.axios.post('api/make_room_free', {
        roomid: this.selected_room
      }).then(res => {
        if (res.data.code === 0) {
          this.updateRoomInfo();
        }
      });
    },
  },

  beforeCreate() {
    this.axios.get('api/get_room_type').then(res => {
      if (res.data.code === 0) {
        for (let i = 0; i < res.data.data.length; i++) {
          this.roomTypes.push(res.data.data[i]['roomtype']);
        }
      }
    });
    this.axios.get('api/get_room_state').then(res => {
      if (res.data.code === 0) {
        this.roomStates = res.data.data;
      }
    });
    this.axios.get('api/get_room_list').then(res => {
      if (res.data.code === 0) {
        this.roomList = res.data.data;
      }
    });
  },

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    },
  },

  watch: {
    dialog(val) {
      val || this.close()
    },
    dialogDelete(val) {
      val || this.closeDelete()
    },
  },

  created() {
    setTimeout(() => {
      for (let i = 0; i < this.roomStates.length; i++) {
        this.roomStateNumber[this.roomStates[i]['statename']] = 0;
        this.state_to_color[this.roomStates[i]['statename']] = this.roomStates[i]['color'];
      }
      for (let i = 0; i < this.roomList.length; i++) {
        this.roomStateNumber[this.roomList[i]['roomstate']]++;
      }
      for (let i = 0; i < this.roomStates.length; i++) {
        this.roomStates[i]['number'] = this.roomStateNumber[this.roomStates[i]['statename']]
      }
      this.initialize()
    }, 500)
  },


}
</script>

<style scoped>

</style>