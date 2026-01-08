# Image Upload & 3D Generation Guide

## What Was Fixed

The image upload feature was creating default cubes instead of using image data. This has been fixed with the following improvements:

### 1. **Better Image Processing**
- Added PIL (Pillow) as primary image loader for better format support
- Added fallback to OpenCV if PIL fails
- Improved error handling and logging for image analysis
- Better color extraction from images

### 2. **Image Analysis Pipeline**
- Detects dominant colors in uploaded images
- Analyzes image complexity and style
- Extracts image dimensions and metadata
- Stores color data in both RGB and hex formats

### 3. **3D Object Generation from Images**
- Uses detected colors to style generated objects
- Adjusts object size based on image complexity
- Properly merges text descriptions with image attributes
- Supports three input modes:
  - **Image only**: Creates object with image-derived properties
  - **Text only**: Creates object as specified in text
  - **Text + Image**: Combines both (image colors/style + text description)

## How to Use the Feature

### Step 1: Upload an Image

1. Click the **📷 camera button** in the command panel at the bottom
2. Select an image from your computer
3. A preview will appear showing the selected file

### Step 2: Describe What to Create (Optional)

You can:
- **Just upload an image** → System creates a 3D object based on image colors/style
- **Add a description** → e.g., "Create a sphere from this image"
- **Give specific instructions** → e.g., "Make this look like an iron suit"

### Step 3: Send and Watch

Click **Send** and Jarvis will:
1. Save your image to the server
2. Analyze the image (colors, complexity, style)
3. Generate a 3D object based on the analysis
4. Render it in the viewport

## Example Workflows

### Workflow 1: Image Only (No Text)
```
1. Click 📷
2. Upload an image (e.g., a red apple photo)
3. Don't type anything
4. Click Send
→ Creates a red object based on image colors
```

### Workflow 2: Describe the Image
```
1. Click 📷
2. Upload an image of iron man armor
3. Type: "Create a 3D model of an iron suit from this image"
4. Click Send
→ Creates a detailed representation using image colors + description
```

### Workflow 3: Simple Style Transfer
```
1. Click 📷
2. Upload any colorful image
3. Type: "Make a sphere"
4. Click Send
→ Creates a sphere with colors from your image
```

## How Image Analysis Works

When you upload an image, the system:

1. **Loads the image** using PIL or OpenCV
2. **Extracts dominant colors** (top 5 colors in the image)
3. **Analyzes complexity** (edge detection and detail level)
4. **Detects dimensions** (width x height)
5. **Analyzes style** (bright/dark, vibrant/muted, etc.)

All this data is converted to 3D object properties:
- **Colors** → Material color of the 3D object
- **Complexity** → Object size and detail level
- **Dimensions** → Aspect ratio hints

## Supported Image Formats

- **JPG/JPEG** - Most common format
- **PNG** - Supports transparency
- **BMP** - Windows bitmap
- **GIF** - Animated images (first frame used)
- **WebP** - Modern web format
- **TIFF** - High-quality images

## Troubleshooting

### Image uploads but no 3D object appears
- Check browser console for error messages
- Make sure the backend is running
- Try a simpler image first (solid colors)

### Object doesn't match image colors
- The system uses the *dominant* color from the image
- Try images with strong, clear colors
- Add a text description to refine the result

### "File upload failed" error
- Check the file size (should be < 50MB)
- Try a different image format
- Ensure you have space on the server

### Backend error logs show image processing failed
- Check that the image file is valid
- Try opening it in an image viewer first
- Make sure dependencies are installed: `pip install -r requirements.txt`

## Advanced Features

### Combining Multiple Images
```
Current: Not supported (uploads one image at a time)
Planned: Batch image processing
```

### Image-to-3D with Complex Objects
```
Current: Simple shapes with image styling
Planned: Advanced models (Shap-E, DreamFusion)
```

### Style Transfer
```
Current: Color-based styling
Planned: Full artistic style transfer
```

## Backend API

The image upload uses two endpoints:

### POST /api/process (multimodal)
```bash
curl -X POST http://localhost:8000/api/process \
  -F "text=Create a sphere from this image" \
  -F "image=@photo.jpg" \
  -F "context_id=optional-scene-id"
```

**Response:**
```json
{
  "context_id": "uuid",
  "result": {
    "actions_executed": 1,
    "results": [
      {
        "status": "success",
        "object": {
          "id": "uuid",
          "type": "sphere",
          "material": {
            "color": "#ff6b6b"
          }
        }
      }
    ]
  },
  "scene": {
    "objects": [...]
  }
}
```

### GET /api/diagnostics
Check system status including image processing capabilities:
```bash
curl http://localhost:8000/api/diagnostics
```

## Performance Notes

- **First image**: May take 2-5 seconds (includes backend startup)
- **Subsequent images**: Usually 1-2 seconds per image
- **Large images**: Automatically resized for processing
- **Backend resource use**: Minimal (color analysis is lightweight)

## Future Improvements

- [ ] Support for batch image processing
- [ ] Integration with advanced text-to-3D models
- [ ] Image-based 3D reconstruction (photogrammetry)
- [ ] Style transfer and artistic filters
- [ ] Video frame extraction
- [ ] Real-time preview of image analysis

## Tips for Best Results

1. **Use clear, distinct colors** → Makes color extraction more accurate
2. **Keep descriptions simple** → "sphere", "cube", "large", "red"
3. **Upload multiple times** → Try different descriptions with same image
4. **Start with primitives** → Before requesting complex objects
5. **Check backend logs** → Helps diagnose processing issues

## Still Having Issues?

Check the server logs for detailed processing information:
```bash
# Terminal where backend is running
# Look for [CV_PROCESSOR] and [ACTION_PLAN] messages
```

Contact support or check [BACKEND_SETUP.md](./BACKEND_SETUP.md) for more help.
