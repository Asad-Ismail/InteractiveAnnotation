<template>
  <div id="app">
    <div class="sidebar">
      <form @submit.prevent="submitForm">
        <label for="class-name">Class Name:</label>
        <select v-model="selectedClass" id="class-name">
          <option v-for="className in classNames" :key="className" :value="className">{{ className }}</option>
        </select>

        <label for="brush-size">Brush Size:</label>
        <input type="number" v-model="brushSize" id="brush-size" />

        <button type="submit">Submit</button>
      </form>
    </div>
    <div class="main">
      <input type="file" @change="loadImage" />
      <img ref="image" :src="imageURL" @mousemove="onMouseMove" />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      classNames: ["Class1", "Class2", "Class3"],
      selectedClass: "",
      brushSize: 5,
      imageURL: "",
    };
  },
  methods: {
    submitForm() {
      console.log("Selected class:", this.selectedClass);
      console.log("Brush size:", this.brushSize);
    },
    loadImage(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageURL = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async onMouseMove(event) {
      const mouseX = event.clientX;
      const mouseY = event.clientY;

      // Request segmentation data from the Flask backend
      try {
        const response = await axios.post("http://localhost:5000/api/segmentation", {
          image: this.imageURL,
          x: mouseX,
          y: mouseY,
          class: this.selectedClass,
          brush_size: this.brushSize,
        });

        const segmentationData = response.data;
        // Update the visualization based on the segmentationData
      } catch (error) {
        console.error("Error fetching segmentation data:", error);
      }
    },
  },
};
</script>

<style>
  /* Add some basic styling */
  #app {
    display: flex;
    height: 100vh;
  }
  .sidebar {
    width: 20%;
    background-color: #f5f5f5;
    padding: 1rem;
    overflow-y: auto;
  }
  .main {
    width: 80%;
    padding: 1rem;
  }
</style>
