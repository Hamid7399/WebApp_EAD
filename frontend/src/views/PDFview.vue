<template>
  <div class="pdf-container">
    <h1>Read Article</h1>
    <iframe
      :src="pdfPath"
      width="100%"
      height="600px"
      style="border:none;"
    ></iframe>
    <br />
    <button @click="$router.push('/dashboard')">Back to Dashboard</button>
  </div>
</template>

<script>
export default {
  name: "PDFview",
  data() {
    return {
      pdfPath: "/Area_of_Triangle.pdf" // served from public/
    };
  }
};
</script>

<style scoped>
.pdf-container {
  padding: 20px;
  text-align: center;
}
button {
  margin-top: 10px;
  padding: 8px 15px;
  cursor: pointer;
}
</style>
