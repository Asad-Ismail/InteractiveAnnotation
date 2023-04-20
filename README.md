# Interactive Annotation Using Segment Anything 🖌️✨


🎉 Welcome to the Interactive Annotation repository!

🌟 This project is all about making segmentation more accessible, faster, accurate and enjoyable for everyone using recently released segement anything model. Let's create an amazing annotation experience together! 🚀


### 📽️ Interactive Annotation "Annotation Mode" in Action
<p align="center">
  <img src="vis_imgs/annotation.gif" alt="Interactive Annotation">
</p>

### 📽️ Interactive Annotation "Preview Mode" Mode
<p align="center">
  <img src="vis_imgs/preview.gif" alt="Interactive Annotation">
</p>


## Disclaimer

⚠️ This project is currently under development. Some features may not be fully functional, and improvements are ongoing. Use at your own risk.

# 🌠 Features

Easy-to-use interface for segmenting images using Segment Anything.

Export annotations in Json formats.

Add custom class names for annotations.

Navigate through images using arrow buttons or arrow keys on the keyboard.

Preview mode or annotation mode.


# 🛠️ Installation

Follow these simple steps to set up the Interactive Annotation tool:

```
chmod +x backend/run_app.sh
chmod +x run_project.sh
```

```
./run_project.sh
```


Install backend dependencies using pip install -r requirments.txt

# 📖 Usage

## Getting Started

1. **Load an image**: Click the "Open Image" button to load an image for annotation.
2. **Preview mode**: By default, the tool is in preview mode, allowing you to explore the image without making annotations.
3. **Annotation mode**: Switch to annotation mode when you're ready to start annotating objects in the image.

## Annotating Objects

1. **Select a class**: Choose the desired class for the object you want to annotate.
2. **Create annotations**: Left-click on various points around the object to create an annotation. The tool will generate a shape that outlines the object.
3. **Refine annotations**: If you need to remove any unnecessary parts of the annotation, right-click on those areas to discard them.
4. **Save object**: Once you're satisfied with the annotation, press the spacebar to save the object.
5. **Save annotations**: To save all the annotations for the current image in JSON format, press Ctrl + S.

## Navigating Images

- **Next image**: Use the right arrow key to move to the next image in the sequence.
- **Previous image**: Use the left arrow key to move to the previous image in the sequence.

## To-Do List

1. Replace pytorch model with onnx model to speed up annotation
2. Add bounding box as an input 
3. Add zoom in and zoom out


# 🤝 How to Contribute

I would absolutely 💖 contributions from community! feel free to contribute from one of to do list or add new feature in our tool

# 📃 License
This project is licensed under the MIT License.

# 🌟 Show Your Support
If you find this project helpful or interesting, please give it a ⭐️ to help it reach more people! And if you have any feedback, ideas, or want to contribute, feel free to open an issue or a pull request. We're always excited to hear from you! 🤗

Happy annotating! 🎉

## References
```
@article{kirillov2023segany,
  title={Segment Anything},
  author={Kirillov, Alexander and Mintun, Eric and Ravi, Nikhila and Mao, Hanzi and Rolland, Chloe and Gustafson, Laura and Xiao, Tete and Whitehead, Spencer and Berg, Alexander C. and Lo, Wan-Yen and Doll{\'a}r, Piotr and Girshick, Ross},
  journal={arXiv:2304.02643},
  year={2023}
}
```