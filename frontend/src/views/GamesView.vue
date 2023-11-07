<template>
  <div>

    <h3>Active games</h3>
    <ul>
      <li v-for="game in games" :key="game.id">
        {{ game.name }} <button @click.prevent="generate_teams">Generate Teams</button>
      </li>
    </ul>

    <h3>Create Game</h3>
    <form @submit.prevent="create_game">
      <label for="game-date">Game Date</label>
      <input type="date" name="game-date" id="game-date" v-model="game.date">
      <br>
      <label for="game-name">Name</label>
      <input type="text" name="game-name" id="game-name" v-model="game.name">
      <br>
      <label for="max-players-per-team">Max Players per Team</label>
      <input type="number" name="max-players-per-team" id="max-players-per-team" v-model="game.max_players_per_team">
      <br>
      <input type="submit" value="Create Game">
    </form>

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
</template>

<script>
export default {
  data() {
    return {
      games: [],
      game: {
        date: null,
        name: null,
        max_players_per_team: null,
        // image: null,
      },
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

    create_game() {
      const url = "http://localhost:8000/game/"
      const data = this.game

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
