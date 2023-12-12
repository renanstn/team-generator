<template>
  <el-table :data="games" stripe>
    <el-table-column prop="name" label="Name" />
    <el-table-column prop="date" label="Date" />
    <el-table-column prop="players.length" label="Players joined" />
    <el-table-column prop="max_players_per_team" label="Player per team" />
    <el-table-column label="Actions" >
      <template #default="scope">
        <el-button type="success" round @click="join_game_visible=true">Join</el-button>
        <el-button type="warning" round>Generate teams</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-dialog title="Enter player name" v-model="join_game_visible" :close-on-click-modal="false">
    <el-form :model="form">
      <el-form-item label="Player name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="join_game_visible=false">Cancel</el-button>
      <el-button type="primary" @click="join_game_visible=false">
        Confirm
      </el-button>
    </template>
  </el-dialog>
</template>


<script>
// import JoinGameModal from '@/components/JoinGameModal.vue'

export default {
  name: 'GameTable',

  components: {
    // JoinGameModal
  },

  props: {
    games: {
      type: Array,
      required: true,
    }
  },

  data() {
    return {
      join_game_visible: false,
      game_id: null,
      form: {
        name: null,
      }
    }
  },

  methods: {
    generate_team(game_id) {
      const url = `http://localhost:8000/generate_teams?game_id=${game_id}`

      fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
      })
    },
  }
}
</script>
