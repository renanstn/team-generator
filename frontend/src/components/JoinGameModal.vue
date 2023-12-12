<template>
  <el-dialog title="Enter player name" v-model="join_game_visible">
    <el-form :model="form">
      <el-form-item label="Player name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="dialogFormVisible = false">Cancel</el-button>
      <el-button type="primary" @click="dialogFormVisible = false">
        Confirm
      </el-button>
    </template>
  </el-dialog>
</template>


<script>
export default {
  props: {
    game_id: Number,
  },

  data() {
    return {
      player: {
        name: null,
        join_game_visible: false
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
