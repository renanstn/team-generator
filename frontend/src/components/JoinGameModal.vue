<template>
  <div id="modal-join-game" class="modal amber lighten-3">
    <div class="modal-content">

      <h3>Join Game</h3>

      <form @submit.prevent="join_game">
        <div class="row">

          <div class="input-field col s12">
            <label for="player-name">Player name</label>
            <input type="text" name="player-name" id="player-name" v-model="player.name">
          </div>

        </div>
      </form>

    </div>
    <div class="modal-footer amber lighten-3">
      <button class="btn waves-effect waves-light amber darken-4 modal-close" @click="join_game">Join</button>
    </div>
  </div>
</template>


<script>
export default {
  props: {
    game_id: Number
  },

  data() {
    return {
      player: {
        name: null
      }
    }
  },

  methods: {
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
        .then(() => {
          this.$emit('onClose')
        })
        .finally(() => {
          this.player.name = null
        })
    }
  },
}
</script>
