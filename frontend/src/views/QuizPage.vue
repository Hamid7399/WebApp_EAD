<template>
  <div class="container">
    <h1>Triangle Quiz</h1>
    <form @submit.prevent="submitQuiz">
      <div v-for="(q, index) in questions" :key="index" class="question">
        <p>{{ index + 1 }}. {{ q.question }}</p>
        <div v-for="(opt, idx) in q.options" :key="idx">
          <label>
            <input 
              type="radio" 
              :name="'q' + index" 
              :value="opt" 
              v-model="answers[index]"
              required
            >
            {{ opt }}
          </label>
        </div>
      </div>

      <button type="submit">Submit</button>
    </form>

    <div v-if="score !== null" class="result">
      <h2>Your Score: {{ score }} / 5</h2>
      <button @click="$router.push('/dashboard')">Back to Dashboard</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuizPage",
  data() {
    return {
      questions: [
        {
          question: "What is the formula for the area of a triangle?",
          options: [
            "(base × height) / 2", 
            "base × height", 
            "2 × (base + height)",
            "(side × side) / 2"
          ],
          answer: "(base × height) / 2"
        },
        {
          question: "A triangle has a base of 8 cm and height of 5 cm. What is its area?",
          options: [
            "20 cm²", 
            "40 cm²", 
            "13 cm²",
            "25 cm²"
          ],
          answer: "20 cm²"
        },
        {
          question: "What is the perimeter of a triangle with sides 5 cm, 6 cm, and 7 cm?",
          options: [
            "18 cm", 
            "16 cm", 
            "17 cm",
            "19 cm"
          ],
          answer: "18 cm"
        },
        {
          question: "If the base is doubled and height is same, the area will...",
          options: [
            "Double", 
            "Stay the same", 
            "Be halved",
            "Increase by four times"
          ],
          answer: "Double"
        },
        {
          question: "A triangle has sides 3 cm, 4 cm, and 5 cm. What is its perimeter?",
          options: [
            "9 cm", 
            "10 cm", 
            "12 cm",
            "11 cm"
          ],
          answer: "12 cm"
        }
      ],
      answers: {},
      score: null
    };
  },
  methods: {
    submitQuiz() {
      // Calculate score
      let points = 0;
      this.questions.forEach((q, index) => {
        if (this.answers[index] === q.answer) {
          points += 1;
        }
      });
      this.score = points;

      // Send score to backend
      const sessionId = localStorage.getItem("sessionId");
      const userId = localStorage.getItem("userId");

      fetch("/api/quiz/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          session_id: sessionId,
          score: points
        }),
      })
      .then(res => res.json())
      .then(data => {
        console.log("Quiz result saved:", data);
      })
      .catch(err => console.error("Error saving quiz result:", err));
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
  padding: 20px;
}
.question {
  margin-bottom: 20px;
}
.result {
  margin-top: 20px;
  padding: 10px;
  background-color: #e7f4e4;
  border: 1px solid #b2d8b2;
}
</style>
