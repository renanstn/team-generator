<template>
  <div class="amber lighten-4">
    <Navbar />
    <CreateGameModal @onClose="load_games" />

    <div class="container">
      <div class="row valign-wrapper">
        <div class="col s9">
          <h4>Active games</h4>
        </div>
        <div class="col s3">
          <a class="waves-effect waves-light btn amber darken-4 modal-trigger" href="#modal-create-game">Create Game</a>
        </div>
      </div>

      <GameTable :games="games" @playerAdd="load_games" />

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
