<template>
  <div id="app">
    <div class="sidebar">
      <div class="logo">
        <img src="path/to/your/logo.png" alt="Your Logo">
      </div>
      <h2>Create New Class</h2>
      <form @submit.prevent="addClass">
        <label for="new-class">New Class Name:</label>
        <input type="text" v-model="newClassName" id="new-class" />
        <button type="submit">Add Class</button>
      </form>
      <hr />
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="class-name">Class Name:</label>
          <select v-model="selectedClass" id="class-name">
            <option v-for="className in classNames" :key="className" :value="className">{{ className }}</option>
          </select>
        </div>
        <label for="files">Choose Files:</label>
        <input type="file" id="files" multiple @change="loadImages" />
        <button type="submit">Submit</button>
      </form>
    </div>
    <div class="main">
      <div class="thumbnails">
        <img
          v-for="(image, index) in imageUrls"
          :key="index"
          class="thumbnail"
          :src="image"
          @click="setCurrentIndex(index)"
        />
      </div>
      <div class="selected-image">
        <button @click="previousImage">&#8249;</button>
        <img ref="image" :src="imageUrls[currentIndex]" @mousemove="onMouseMove" />
        <button @click="nextImage">&#8250;</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      classNames: ["SomeClass"],
      selectedClass: "",
      imageUrls: [],
      newClassName: "",
      currentIndex: 0,
    };
  },
  methods: {
    submitForm() {
      console.log("Selected class:", this.selectedClass);
    },
    setCurrentIndex(index) {
    this.currentIndex = index;
  },
  previousImage() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
    }
  },
  nextImage() {
    if (this.currentIndex < this.imageUrls.length - 1) {
      this.currentIndex++;
    }
  },
    loadImages(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.imageUrls = [];
        for (const file of files) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.imageUrls.push(e.target.result);
          };
          reader.readAsDataURL(file);
        }
      }
    },
    async onMouseMove(event) {
      const mouseX = event.clientX;
      const mouseY = event.clientY;

      // Request segmentation data from the Flask backend
      try {
        const response = await axios.post("http://localhost:5000/api/segmentation", {
          image: this.imageUrls,
          x: mouseX,
          y: mouseY,
          class: this.selectedClass,
        });

        // eslint-disable-next-line no-unused-vars
        const segmentationData = response.data;
        // Update the visualization based on the segmentationData
      } catch (error) {
        console.error("Error fetching segmentation data:", error);
      }
    },
    addClass() {
      if (this.newClassName.trim() !== "" && !this.classNames.includes(this.newClassName.trim())) {
        this.classNames.push(this.newClassName.trim());
        this.newClassName = "";
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
    width: 100vw;
    font-family: Arial, sans-serif;
  }
  .sidebar {
    width: 20%;
    min-height: 100vh;
    background-color: #4a69bd;
    padding: 1rem;
    overflow-y: auto;
    color: #fff;
  }
  .sidebar h2 {
    margin-top: 0;
  }
  .sidebar hr {
    border-color: #fff;
  }
  .sidebar label {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }
  .sidebar input,
  .sidebar select {
    width: 100%;
    padding: 0.5rem;
    font-size: 1.1rem;
    border-radius: 5px;
    border: 4px solid #f6b93b;
    background-color: rgba(246, 185, 59, 0.2);
    color: #fff;
    margin-bottom: 1rem;
    box-sizing: border-box;
    transition: background-color 0.3s, border-color 0.3s;
  }
  .sidebar input:hover,
  .sidebar select:hover {
    background-color: rgba(246, 185, 59, 0.4);
    border-color: #fa983a;
  }
  .sidebar input:focus,
  .sidebar select:focus {
    outline: none;
    background-color: rgba(246, 185, 59, 0.4);
    border-color: #fa983a;
  }
  .sidebar button {
    width: 100%;
    padding: 0.75rem;
    font-size: 1.2rem;
    background-color: #f6b93b;
    border: none;
    color: #fff;
    cursor: pointer;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    font-weight: bold;
    margin-bottom: 3rem;
    transition: background-color 0.3s;
  }
  .sidebar button:hover {
    background-color: #fa983a;
  }
  .sidebar .form-group {
    display: flex;
    flex-direction: column;
  }

  .main {
  width: 65%;
  min-height: 100vh;
  padding: 1rem;
  background-color: #82ccdd;
  display: flex;
  flex-direction: column;
  align-items: center;
  }
  .selected-image {
    width: 100%;
    height: calc(100vh - 4rem);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: auto;
  }
  input[type="file"] {
    margin-bottom: 1rem;
  }
  img {
    max-width: 100%;
    max-height: 100%;
  }
  .thumbnails {
    display: flex;
    flex-wrap: nowrap;
    gap: 1rem;
    margin-bottom: 1rem;
    overflow-x: auto;
  }
  .thumbnail {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border: 2px solid #ccc;
    cursor: pointer;
  }
  .thumbnail:hover {
    border-color: #007bff;
  }
  .selected-image img {
    max-width: 100%;
    max-height: calc(100vh - 4rem);
    object-fit: contain;
  }
  .selected-image button {
    font-size: 2rem;
    background: none;
    border: none;
    cursor: pointer;
    transition: color 0.3s;
  }
  .selected-image button:hover {
    color: #007bff;
  }
  .selected-image button:focus {
    outline: none;
  }
  .logo {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.logo img {
  max-width: 80%;
  max-height: 80px;
}
</style>

