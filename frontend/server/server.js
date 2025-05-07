const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());

// Set storage destination and filename for images
const storage = multer.diskStorage({
  destination: "public/uploads/",
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname)); // Unique name
  },
});

const upload = multer({ storage });

// Upload route
app.post("/upload", upload.single("image"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No file uploaded!" });
  }
  res.json({ message: "File uploaded successfully!", file: req.file.filename });
});

// Serve static files
app.use("/uploads", express.static("public/uploads"));

// Start server
app.listen(5000, () => console.log("Server running on port 5000"));
