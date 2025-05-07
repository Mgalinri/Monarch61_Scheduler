import { join, extname } from "path";
import sharp from "sharp";

export default defineEventHandler(async (event) => {
  const form = await readMultipartFormData(event);
  
  if (!form || !form[0]) {
    return { error: "No file uploaded!" };
  }

  const file = form[0]; // First uploaded file
  const originalExt = extname(file.filename); // Get original file extension
  const newFileName = file.filename.replace(originalExt, ".webp"); // Convert filename to .webp
  const filePath = join("public/uploads", newFileName); // Save in /public/uploads/

  try {
    // Remove original file before conversion
    // const tempPath = join("public/uploads", file.filename);
    // unlinkSync(tempPath);
    // Convert image to .webp using sharp
    await sharp(file.data)
      .webp({ quality: 80 }) // Convert to webp with quality 80
      .toFile(filePath);
    
    return { message: "File uploaded & converted to .webp!", file: newFileName };
  } catch (error) {
    console.error("Conversion error:", error);
    return { error: "Image conversion failed!" };
  }
});
