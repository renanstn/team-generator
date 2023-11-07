<template>
    <table class="striped">
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
          <td>0</td>
          <td>
            <a class="waves-effect waves-light btn amber darken-4">Join</a>
            <a class="waves-effect waves-light btn amber darken-4" style="margin-left: 10px;">Generate Teams</a>
          </td>
        </tr>
      </tbody>
    </table>
</template>

<script>
export default {
  name: 'GameTable',
  props: {
    games: {
      type: Array,
      required: true,
    }
  }
}
</script>
