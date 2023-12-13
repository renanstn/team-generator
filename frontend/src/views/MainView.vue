<template>
  <el-container>
    <el-header>
      <el-row class="navbar" align="middle">
        <el-col :span="12">
          <h1>Team Generator</h1>
        </el-col>
        <el-col :span="12" class="login-button">
          <el-button type="primary" round @click="open_login_modal">Login</el-button>
        </el-col>
      </el-row>
    </el-header>

    <el-main>
      <el-row align="middle">
        <el-col :span="12">
          <h3>Active games</h3>
        </el-col>

        <el-col :span="12" class="create-game-button">
          <el-button type="primary" round @click="create_game_visible=true">
            Create game
          </el-button>
        </el-col>
      </el-row>

      <el-table :data="games" stripe>
        <el-table-column prop="name" label="Name" />
        <el-table-column prop="date" label="Date" />
        <el-table-column prop="players.length" label="Players joined" />
        <el-table-column prop="max_players_per_team" label="Player per team" />
        <el-table-column label="Actions" >
          <template #default="scope">
            <el-button type="success" round @click="open_join_game_modal(scope.row.id)">
              Join
            </el-button>
            <el-button type="warning" round>Generate teams</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Login modal ---------------------------------------------------- -->
      <el-dialog
        title="Login"
        v-model="login_visible"
        :close-on-click-modal="false"
        @opened="handle_login_modal_opened"
      >
        <el-form :model="login_form" label-position="top" @submit.prevent="login">

          <el-form-item label="User" prop="user">
            <el-input v-model="login_form.user" placeholder="Type your username" ref="user_input" />
          </el-form-item>

          <el-form-item label="Password" prop="pass">
            <el-input type="password" v-model="login_form.pass" placeholder="Type your password" show-password />
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="login_visible=false">Cancel</el-button>
          <el-button type="primary" @click="login">Confirm</el-button>
        </template>
      </el-dialog>

      <!-- Create game modal ---------------------------------------------- -->
      <el-dialog
        title="Create game"
        v-model="create_game_visible"
        :close-on-click-modal="false"
      >
        <el-form :model="game_form" label-position="top" :rules="rules">

          <el-form-item label="Date" prop="date">
            <el-date-picker
              v-model="game_form.date"
              type="date"
              placeholder="Pick a day"
              format="DD/MM/YYYY"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>

          <el-form-item label="Name" prop="name">
            <el-input v-model="game_form.name" placeholder="Type a name"/>
          </el-form-item>

          <el-form-item label="Max player per team">
            <el-input-number v-model="game_form.max_players_per_team" :min="1"/>
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="create_game_visible = false">Cancel</el-button>
          <el-button type="primary" @click="create_game">Confirm</el-button>
        </template>
      </el-dialog>

      <!-- Join game modal ------------------------------------------------ -->
      <el-dialog
        title="Enter player name"
        v-model="join_game_visible"
        :close-on-click-modal="false"
        @opened="handle_join_game_opened"
      >
        <el-form :model="join_form" @submit.prevent="join_game">
          <el-form-item label="Player name">
            <el-input v-model="join_form.name" ref="player_name" />
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="join_game_visible=false">Cancel</el-button>
          <el-button type="primary" @click="join_game">Confirm</el-button>
        </template>
      </el-dialog>

    </el-main>
  </el-container>
</template>


<style scoped>
.navbar {
  background-color: #e0e9f0;
  padding-left: 10px;
  padding-right: 10px;
}
.login-button {
  text-align: right;
}
.create-game-button {
  text-align: right;
}
</style>


<script>
import { ElMessage } from 'element-plus'

export default {
  data() {
    return {
      game_id: null,
      games: [],
      player: {
        name: null,
      },
      create_game_visible: false,
      join_game_visible: false,
      login_visible: false,
      login_form: {
        user: null,
        pass: null,
      },
      join_form: {
        name: null,
      },
      game_form: {
        date: null,
        name: null,
        max_players_per_team: 1,
      },
      rules: {
        name: [{required: true, message: 'Please input your name', trigger: 'blur'}],
        date: [{required: true, message: 'Please pick a date', trigger: 'blur'}],
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

    open_join_game_modal(game_id) {
      this.game_id = game_id
      this.join_game_visible = true
    },

    open_login_modal() {
      this.login_visible = true
    },

    handle_login_modal_opened() {
      this.$refs.user_input.focus()
    },

    login() {
      console.log('TODO')
    },

    handle_join_game_opened() {
      this.$refs.player_name.focus()
    },

    join_game() {
      const url = `http://localhost:8000/player?game_id=${this.game_id}`
      const data = this.join_form

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
          ElMessage({message: 'Player joined!', type: 'success'})
        })
        .finally(() => {
          for (const i in this.join_form) { this.join_form[i] = null }
          this.load_games()
          this.join_game_visible = false
        })
    },

    generate_team(game_id) {
      const url = `http://localhost:8000/generate_teams?game_id=${game_id}`

      fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
      })
    },

    create_game() {
      const url = "http://localhost:8000/game/"
      const data = this.game_form

      fetch(url, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(response => {
          if (!response.ok) { throw new Error('Error sendind request') }
          return response.json()
        })
        .finally(() => {
          this.create_game_visible = false
          this.load_games()
        })
    },
  },
}
</script>
