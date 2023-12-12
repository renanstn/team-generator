<template>
  <el-row class="navbar" align="middle">
    <el-col :span="12">
      <h1>Team Generator</h1>
    </el-col>
    <el-col :span="12" class="login-button">
      <el-button type="primary" round>Login</el-button>
    </el-col>
  </el-row>
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
</style>
