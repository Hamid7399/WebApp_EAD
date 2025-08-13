<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="login" class="login-form">
      <input type="text" placeholder="Username" v-model="username" required />
      <input type="password" placeholder="Password" v-model="password" required />
      <button type="submit">Login</button>
    </form>
    <p class="message" v-if="message">{{ message }}</p>
    <p>
      Don't have an account?
      <router-link to="/signup">Sign up here</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      message: ""
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });

        const data = await response.json();
        this.message = data.message;

        if (data.message === "Login successful") {
          localStorage.setItem("userId", data.user_id);
          localStorage.setItem("username", data.username);
          this.$router.push("/dashboard");
        }
      } catch (error) {
        console.error("Error logging in:", error);
        this.message = "An error occurred while logging in.";
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.login-form input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.login-form button {
  padding: 10px;
  font-size: 16px;
  background: #007BFF;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.login-form button:hover {
  background: #0056b3;
}

.message {
  margin-top: 10px;
  color: red;
  font-size: 14px;
}
</style>
