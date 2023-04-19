    drawMask(maskData)
    {
    if (!maskData || maskData.length === 0) {
      console.error("Mask data is empty or undefined");
      return;
    }
    //console.log('maskData:', maskData); // Add this line to log the mask data 
    // Merge previous data with current
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