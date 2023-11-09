<template>
  <div class="amber lighten-4">
    <Navbar/>
    <CreateGameModal/>

    <div class="container">
      <div class="row valign-wrapper">
        <div class="col s9">
          <h4>Active games</h4>
        </div>
        <div class="col s3">
          <a class="waves-effect waves-light btn amber darken-4 modal-trigger" href="#modal-create-game">Create Game</a>
        </div>
      </div>

      <GameTable :games="games"/>

      <h3>Join Game</h3>
      <form @submit.prevent="join_game">
        <label for="game-id">Game ID</label>
        <input type="number" name="game-id" id="game-id" v-model="game_id">
        <br>
        <label for="player-name">Player Name</label>
        <input type="text" name="player-name" id="player-name" v-model="player.name">
        <br>
        <input type="submit" value="Join Game">
      </form>
    </div>

  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import GameTable from '@/components/GameTable.vue'
import CreateGameModal from '@/components/CreateGameModal.vue'

export default {
  components: {
    Navbar,
    GameTable,
    CreateGameModal
  },

  data() {
    return {
      games: [],
      game_id: null,
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
        if (!response.ok) {throw new Error("Error getting games from API.")}
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
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      })
      .then(response => {
        if (!response.ok) {throw new Error('Error sendind request')}
        return response.json()
      })
      .then(data => {
        console.log(data)
        this.load_games()
      })
    }
  },
}
</script>
