<template>
  <table class="striped">
    <JoinGameModal :game_id="game_id" @onClose="emit_update" />
    <thead>
      <tr>
        <th>Name</th>
        <th>Date</th>
        <th>Players</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="game in games" :key="game.id">
        <td>{{ game.name }}</td>
        <td>{{ game.date }}</td>
        <td class="tooltipped" data-tooltip="I am a tooltip">{{ game.players.length }}</td>
        <td>
          <a class="waves-effect waves-light btn amber darken-4 modal-trigger" href="#modal-join-game"
            @click="game_id = game.id">Join</a>
          <a class="waves-effect waves-light btn amber darken-4" style="margin-left: 10px;" @click="generate_team(game.id)">Generate Teams</a>
        </td>
      </tr>
    </tbody>
  </table>
</template>


<script>
import JoinGameModal from '@/components/JoinGameModal.vue'

export default {
  name: 'GameTable',

  components: {
    JoinGameModal
  },

  props: {
    games: {
      type: Array,
      required: true,
    }
  },

  data() {
    return {
      game_id: null
    }
  },

  methods: {
    emit_update() {
      this.$emit('playerAdd')
    },

    generate_team(game_id) {
      console.log(game_id);
    },
  }
}
</script>
