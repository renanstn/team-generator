<template>
  <el-container>
    <el-header>
      <Navbar />
    </el-header>

    <!-- <CreateGameModal @onClose="load_games" /> -->

    <el-main>
      <el-row align="middle">
        <el-col :span="12">
          <h3>Active games</h3>
        </el-col>

        <el-col :span="12" class="create-game-button">
          <el-button type="primary" round @click="create_game_visible=true">
            Create game
          </el-button>
        </el-col>
      </el-row>

      <GameTable :games="games" />

      <el-dialog
        title="Create game"
        v-model="create_game_visible"
        :close-on-click-modal="false"
      >
        <el-form :model="game_form" label-position="top" :rules="rules">

          <el-form-item label="Date" prop="date">
            <el-date-picker
              v-model="game_form.date"
              type="date"
              placeholder="Pick a day"
              format="DD/MM/YYYY"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>

          <el-form-item label="Name" prop="name">
            <el-input v-model="game_form.name" placeholder="Type a name"/>
          </el-form-item>

          <el-form-item label="Max player per team">
            <el-input-number v-model="game_form.max_players_per_team" :min="1"/>
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="create_game_visible = false">Cancel</el-button>
          <el-button type="primary" @click="create_game">Confirm</el-button>
        </template>
      </el-dialog>

    </el-main>
  </el-container>
</template>


<style scoped>
.create-game-button {
  text-align: right;
}
</style>


<script>
import Navbar from '@/components/Navbar.vue'
import GameTable from '@/components/GameTable.vue'
import CreateGameModal from '@/components/CreateGameModal.vue'

export default {
  components: {
    Navbar,
    GameTable,
    CreateGameModal,
  },

  data() {
    return {
      games: [],
      player: {
        name: null,
      },
      create_game_visible: false,
      game_form: {
        date: null,
        name: null,
        max_players_per_team: 1,
      },
      rules: {
        name: [{required: true, message: 'Please input your name', trigger: 'blur'}],
        date: [{required: true, message: 'Please pick a date', trigger: 'blur'}],
      }
    }
  },

  mounted() {
    this.load_games()
  },

  methods: {
    load_games() {
      const url = "http://localhost:8000/games"
      fetch(url).then(response => {
        if (!response.ok) { throw new Error("Error getting games from API.") }
        return response.json()
      })
        .then(data => {
          this.games = data
        })
        .catch(error => {
          console.log("Error on load games:", error)
        })
    },

    join_game() {
      const url = `http://localhost:8000/player?game_id=${this.game_id}`
      const data = this.player

      fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(response => {
          if (!response.ok) { throw new Error('Error sendind request') }
          return response.json()
        })
        .then(data => {
          this.load_games()
        })
    },

    create_game() {
      const url = "http://localhost:8000/game/"
      const data = this.game_form
      console.log(this.game_form.date);

      fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(response => {
          if (!response.ok) { throw new Error('Error sendind request') }
          return response.json()
        })
        .finally(() => {
          this.create_game_visible = false
          this.load_games()
        })
    },
  },
}
</script>
