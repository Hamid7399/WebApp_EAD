<template>
  <div class="container">
    <h1>Welcome to Dashboard</h1>
    <div class="card-row">
      
      <!-- PDF Card -->
      <div class="card click-track">
        <router-link to="/pdf" class="card-link">
          📄 <span>Read Article (PDF)</span>
        </router-link>
      </div>

      <!-- Video Card with Click Overlay -->
      <div class="card click-track video-card">
        <div 
          class="video-overlay click-track" 
          data-description="Watch Video"
          @click="removeOverlay"
        >
          ▶ Watch Video
        </div>
        <iframe 
          width="100%" 
          height="200" 
          src="https://www.youtube.com/embed/YOYQys52sPs?enablejsapi=1"
          frameborder="0"
          allowfullscreen>
        </iframe>
      </div>

      <!-- Quiz Card -->
      <div class="card click-track">
        <router-link to="/quiz" class="card-link">
          📝 <span>Take Quiz</span>
        </router-link>
      </div>

    </div>

    <button @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  name: "UserDashboard",
  methods: {
    removeOverlay(event) {
      // Hide overlay after first click
      event.target.style.display = "none";
    },
    logout() {
      localStorage.removeItem("userId");
      localStorage.removeItem("username");
      localStorage.removeItem("sessionId");
      sessionStorage.clear();
      window.location.href = "/login";
    }
  }
};
</script>

<style scoped>
.card-row {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.card {
  flex: 1;
  background: #f8f8f8;
  padding: 0;
  text-align: center;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-link {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 20px;
  text-decoration: none;
  color: #007BFF;
  font-weight: bold;
}

.card-link span {
  margin-top: 10px;
}

.video-card {
  position: relative;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  z-index: 2;
}

.card iframe {
  border-radius: 6px;
}
</style>
