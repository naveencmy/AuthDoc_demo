const multer = require("multer");

/**
 * Upload middleware
 * Handles file ingestion only
 */
const upload = multer({
  dest: "uploads/"
});

module.exports = upload;
