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
          <el-button type="primary" round>Create game</el-button>
        </el-col>
      </el-row>

      <GameTable :games="games" />

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
    }
  },
}
</script>
