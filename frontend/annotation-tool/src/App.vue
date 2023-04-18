<template>
  <div id="app">
    <div class="sidebar">
      <div class="logo">
        <img :src="require('@/assets/logo.jpeg')" alt="Your Logo">
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
      <div class="action-buttons">
        <button @click="enablePreview" :class="{ active: isPreviewEnabled }">Preview</button>
        <button @click="enableAnnotation" :class="{ active: !isPreviewEnabled }">Annotation</button>
      </div>
      <button @click="undoAnnotation" class="btn btn-danger">Undo</button>
      <button @click="clearAll" class="btn btn-warning">Clear All</button>
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
        <div class="image-navigation">
          <button @click="previousImage">&#8249;</button>
          <div class="image-container">
            <img ref="image" :src="imageUrls[currentIndex]" @mousemove="onMouseMove" @mousedown="onMouseDown" @contextmenu.prevent style="z-index: 1;" />
            <canvas ref="canvas" width="0" height="0" @mousemove="onMouseMove" @mousedown="onMouseDown" @contextmenu.prevent style="z-index: 2;"></canvas>
          </div>
          <button @click="nextImage">&#8250;</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      classNames: ["Stuff"],
      selectedClass: "",
      imageUrls: [],
      newClassName: "",
      currentIndex: 0,
      debounceTimeout: null,
      isPreviewEnabled: true,
      clicksData: [],
    };
  },
  mounted() {
    window.addEventListener("keydown", this.handleKeydown);
    document.addEventListener("keydown", this.onKeydown);
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeydown);
    document.removeEventListener("keydown", this.onKeydown);
  },
  methods: {
  submitForm() {
      console.log("Selected class:", this.selectedClass);
  },
  setCurrentIndex(index) {
    this.currentIndex = index;
    this.sendImageToBackend(); // Add this line to send the image to the backend
  },
  async sendImageToBackend() {
  try {
    await axios.post("http://localhost:5000/api/load_image", {
      image: this.imageUrls[this.currentIndex],
    });
  } catch (error) {
    console.error("Error sending image to backend:", error);
  }
  },
  previousImage() {
    if (this.currentIndex > 0) {
      this.clearCanvas(); // Add this line to clear the canvas
      this.currentIndex--;
      this.sendImageToBackend();
    }
  },
  nextImage() {
    if (this.currentIndex < this.imageUrls.length - 1) {
      this.clearCanvas(); // Add this line to clear the canvas
      this.currentIndex++;
      this.sendImageToBackend();
    }
  },
  enablePreview() {
    this.isPreviewEnabled = true;
    this.clearCanvas();
  },
  enableAnnotation() {
    this.isPreviewEnabled = false;
    this.clearCanvas();
  },
  loadImages(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.imageUrls = [];
        for (const file of files) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.imageUrls.push(e.target.result);
            this.sendImageToBackend(); // Add this line to send the image to the backend
          };
          reader.readAsDataURL(file);
        }
      }
    },
    clearCanvas() {
    const canvas = this.$refs.canvas;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    },
    handleKeydown(event) {
    if (event.key === "ArrowRight") {
      this.nextImage();
    } else if (event.key === "ArrowLeft") {
      this.previousImage();
    }
    },
    async onKeydown(event) {
    if (event.ctrlKey && event.key === "s") {
      event.preventDefault();
      console.log("Saving Annotation and clearing clicks data:");
      try {
      const response = await axios.post("http://localhost:5000/api/annotation", {
        annotations: this.clicksData,
        save_res: true,
      });
      console.log(`Saving Annotations sent: click data=${this.clicksData}`);
      const segmentationData = response.data;
      this.drawMask(segmentationData,false);
    } catch (error) {
      console.error("Error sending annotation data:", error);
    }
      // click annotations
      this.clicksData = [];
    }
    else if (event.key === " ") {
      // Handle space key press event
      console.log("Done with current object segmentation");
      event.preventDefault();
      console.log("Saving Annotation and clearing clicks data:");
      try {
      const response = await axios.post("http://localhost:5000/api/annotation", {
        annotations: this.clicksData,
        done_obj: true,
      });
      console.log(`Done current Annotation sent: click data=${this.clicksData}`);
      const segmentationData = response.data;
      this.drawMask(segmentationData,false);
    } catch (error) {
      console.error("Error sending annotation data:", error);
    }
      // click annotations
      this.clicksData = [];
    }
    },
    clearAll() {
    this.clicksData= [];
    // Clear canvas if needed
    },
    // method to draw the mask data on the canvas
    drawMask(maskData,clearCanvas = true)
    {
    if (!maskData || maskData.length === 0) {
      console.error("Mask data is empty or undefined");
      return;
    }
    //console.log('maskData:', maskData); // Add this line to log the mask data
    const image = this.$refs.image;
    const rect = image.getBoundingClientRect();
    const scaleX = image.naturalWidth / rect.width;
    const scaleY = image.naturalHeight / rect.height;

    const canvas = this.$refs.canvas;
    canvas.width = image.width;
    canvas.height = image.height;
    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    const selectedClassColor = 'rgba(255, 0, 0, 0.5)'; // Set the color for the selected class
    if (clearCanvas) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    // Add variables to count the number of mask pixels drawn
    let drawnPixels = 0;
    let totalPixels = 0;
    for (let i = 0; i < height; i++) {
      for (let j = 0; j < width; j++) {
        // Get the corresponding mask data based on scaleX and scaleY
        const maskX = Math.round(j * scaleX);
        const maskY = Math.round(i * scaleY);
        const maskValue = maskData[maskY][maskX];
        if (maskValue) {
          ctx.fillStyle = selectedClassColor; // Use the selected class color for the boolean mask
          ctx.fillRect(j, i, 1, 1);
          drawnPixels++; // Increment drawnPixels
        }
        totalPixels++; // Increment totalPixels
      }
    }
    console.log('Mask drawn on canvas.'); // Log message for mask drawing
    // Log the number of drawn mask pixels
    console.log(`Drawn pixels: ${drawnPixels} / ${totalPixels}`);
  },

  onMouseMove(event) {
    // on mouse only works on preview mode
    if (!this.isPreviewEnabled) return;
    clearTimeout(this.debounceTimeout);
    this.debounceTimeout = setTimeout(async () => {
      const image = this.$refs.image;
      const rect = image.getBoundingClientRect();
      const scaleX = image.naturalWidth / rect.width;
      const scaleY = image.naturalHeight / rect.height;

      const mouseX = event.clientX - rect.left;
      const mouseY = event.clientY - rect.top;

      const imageX = Math.round(mouseX * scaleX);
      const imageY = Math.round(mouseY * scaleY);

      // Request segmentation data from the Flask backend
      try {
        const response = await axios.post("http://localhost:5000/api/segmentation", {
          x: imageX,
          y: imageY,
          class: this.selectedClass,
        });

        const segmentationData = response.data;
        this.drawMask(segmentationData);
      } catch (error) {
        console.error("Error fetching segmentation data:", error);
      }
    },500); // 500ms debounce
  },

  async onMouseDown(event) {
    if (this.isPreviewEnabled) return;

    const image = this.$refs.image;
    const rect = image.getBoundingClientRect();
    const scaleX = image.naturalWidth / rect.width;
    const scaleY = image.naturalHeight / rect.height;

    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    const imageX = Math.round(mouseX * scaleX);
    const imageY = Math.round(mouseY * scaleY);

    let label = -1;

    if (event.button === 0) {
      label = 1;
    } else if (event.button === 2) {
      label = 0;
    } else {
      return;
    }
    this.clicksData.push({
    x: imageX,
    y: imageY,
    class: this.selectedClass,
    label: label,
    });
    try {
      const response = await axios.post("http://localhost:5000/api/annotation", {
        annotations: this.clicksData,
      });
      console.log(`Annotation sent: x=${imageX}, y=${imageY}, class=${this.selectedClass}, label=${label}`);
      const segmentationData = response.data;
      // Add this line for debugging
      //console.log("Received mask data:", segmentationData);
      this.drawMask(segmentationData,false);
    } catch (error) {
      console.error("Error sending annotation data:", error);
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
  position: relative; /* Add this line */
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

.selected-image img,
.selected-image canvas {
  position: absolute;
  top: 0;
  left: 0;
  max-width: 100%;
  max-height: calc(100vh - 4rem);
  object-fit: contain;
  z-index: 1;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.action-buttons button {
  background-color: #f6b93b;
  border: none;
  color: #fff;
  cursor: pointer;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

.action-buttons button:hover {
  background-color: #fa983a;
}

.action-buttons button.active {
  background-color: #fa983a;
}
</style>