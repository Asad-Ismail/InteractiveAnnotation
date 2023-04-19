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
    max-height: 100%;
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