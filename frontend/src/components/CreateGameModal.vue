<template>
  <div id="modal-create-game" class="modal amber lighten-3">
    <div class="modal-content">

      <h3>Create Game</h3>

      <form @submit.prevent="create_game">
        <div class="row">

          <div class="input-field col s3">
            <label for="game-date">Game Date</label>
            <input type="date" name="game-date" id="game-date" v-model="game.date">
          </div>

          <div class="input-field col s6">
            <label for="game-name">Name</label>
            <input type="text" name="game-name" id="game-name" v-model="game.name">
          </div>

          <div class="input-field col s3">
            <label for="max-players-per-team">Max Players per Team</label>
            <input type="number" name="max-players-per-team" id="max-players-per-team"
              v-model="game.max_players_per_team">
          </div>
        </div>
      </form>

    </div>
    <div class="modal-footer amber lighten-3">
      <button class="btn waves-effect waves-light amber darken-4 modal-close" @click="create_game">Create</button>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      game: {
        id: null,
        date: null,
        name: null,
        max_players_per_team: null,
        // image: null,
      },
    }
  },

  mounted() {
    // Init modals component
    var modal_elements = document.querySelectorAll('.modal')
    M.Modal.init(modal_elements)
  },

  methods: {
    update_date(event) {
      console.log('plim');
      this.game.date = event.target.value
    },

    create_game() {
      const url = "http://localhost:8000/game/"
      const data = this.game
      console.log(data);

      fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(response => {
          if (!response.ok) { throw new Error('Error sendind request') }
          return response.json()
        })
        .then(_ => {
          this.$emit('onClose')
        })
    },
  }
}
</script>
