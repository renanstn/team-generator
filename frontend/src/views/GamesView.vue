<template>
  <div>
    <h3>Active games</h3>
    <ul>
      <li v-for="game in games">{{ game.name }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      games: [
        { "id": 1, "name": "Game A" },
        { "id": 2, "name": "Game B" },
        { "id": 3, "name": "Game C" },
      ]
    }
  }
}
</script>
