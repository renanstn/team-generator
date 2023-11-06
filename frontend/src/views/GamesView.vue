<template>
  <div>

    <h3>Active games</h3>
    <ul>
      <li v-for="game in games" :key="game.id">{{ game.name }}</li>
    </ul>

    <h3>Create Game</h3>
    <form @submit.prevent="create_game">
      <label for="game-date">Game Date</label>
      <input type="date" name="game-date" id="game-date">
      <br>
      <label for="game-name">Name</label>
      <input type="text" name="game-name" id="game-name">
      <br>
      <label for="max-players-per-team">Max Players per Team</label>
      <input type="number" name="max-players-per-team" id="max-players-per-team">
      <br>
      <input type="submit" value="Create Game">
    </form>

    <h3>Join Game</h3>
    <form @submit.prevent="join_game">
      <label for="game-id">Game ID</label>
      <input type="number" name="game-id" id="game-id">
      <br>
      <label for="player-name">Player Name</label>
      <input type="text" name="player-name" id="player-name">
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
        name: null,
        max_players_per_team: null
      },
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
      const url = "http://localhost:8000/game"
      const data = {
        name: this.game.name,
        max_players_per_team: this.game.max_players_per_team,
      }

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
      })
    },

    join_game() {
      console.log('join game')
    }
  },
}
</script>
