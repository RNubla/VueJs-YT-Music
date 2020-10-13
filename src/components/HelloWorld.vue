<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <form action="" method="post" @submit.prevent="AddToList">
      <p>
        <input type="text" v-model="yturl" />
        <button type="submit">Submit</button>
      </p>
    </form>
    <Aplayer
      slot="display"
      :key="songs"
      autoplay
      :list="songs"
      :music="songs[0]"
      ref="player"
    />
  </div>
</template>

<script>
const axios = require("axios");
const API_URL = "http://localhost:5000";

import Aplayer from "vue-aplayer";
export default {
  name: "HelloWorld",
  data() {
    return {
      yturl: null,
      ytid: "",
      songs: [
        {
          artist: "",
          pic: "",
          src: "",
          title: ""
        }
      ]
    };
  },
  async mounted() {
    try {
      const res = await axios.get(`${API_URL}/songs`);
      this.songs = res.data;
      console.log(res.data);
    } catch (error) {
      console.error(error);
    }
    /* axios
      .get(`${API_URL}/songs`)
      .then(res => {
        this.songs = res.data;
        console.log(res.data);
      })
      .catch(error => console.log(error)); */
  },

  components: {
    Aplayer
  },
  watch: {
    yturl() {
      this.yturl = this.yturl
        .replace(/(>|<)/gi, "")
        .split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
      if (this.yturl[2] !== undefined) {
        this.ytid = this.yturl[2].split(/[^0-9a-z_-]/i);
        this.ytid = this.ytid[0];
      } else {
        this.ytid = this.yturl;
      }
      return this.ytid;
    }
  },
  methods: {
    async getList() {
      axios
        .get(`${API_URL}/songs`)
        .then(res => {
          this.songs = res.data;
        })
        .catch(error => console.log(error));
    },
    async AddToList() {
      axios
        .post(`${API_URL}/${this.ytid}`, this.ytid)
        .then(res => {
          res = this.ytid;
          this.getList();
          console.log(res);
        })
        .catch(error => console.log(error));
    }
  },
  props: {
    msg: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
