const express = require("express");
const upload = require("../middleware/upload.middleware");
const controller = require("../controllers/verify.controller");

const router = express.Router();

router.post("/ingest", upload.single("file"), controller.ingest);
router.post("/verify", controller.verifySingle);
router.post("/verify/batch", controller.verifyBatch);

module.exports = router;
