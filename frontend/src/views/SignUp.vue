<template>
  <div class="signup-container">
    <h1>Sign Up</h1>
    <form @submit.prevent="signup" class="signup-form">
      <input type="text" placeholder="Full Name" v-model="name" required />
      <input type="text" placeholder="Username" v-model="username" required />
      <input type="password" placeholder="Password" v-model="password" required />
      <button type="submit">Sign Up</button>
    </form>
    <p>
      Already have an account?
      <router-link to="/login">Login here</router-link>
    </p>
    <p class="message" v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: "SignUpPage",
  data() {
    return {
      name: "",
      username: "",
      password: "",
      message: ""
    };
  },
  methods: {
    async signup() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name: this.name,
            username: this.username,
            password: this.password
          })
        });

        const data = await response.json();
        this.message = data.message;

        if (data.message === "User created successfully") {
          this.$router.push("/login");
        }
      } catch (error) {
        console.error("Error signing up:", error);
      }
    }
  }
};
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.signup-container h1 {
  margin-bottom: 20px;
  font-size: 24px;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.signup-form input {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.signup-form button {
  padding: 10px;
  font-size: 16px;
  background: #007BFF;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.signup-form button:hover {
  background: #0056b3;
}

.message {
  margin-top: 10px;
  color: green;
}
</style>
