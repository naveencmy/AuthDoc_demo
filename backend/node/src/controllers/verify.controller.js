const{randomUUID}=require("crypto");
const policies = require("../config/policies.json");
const store = require("../store/documentStore");
const { sendToOCR } = require("../services/pythonClient");
const { verify } = require("../services/verifier.service");

/**
 * Ingest document → OCR → store extracted data
 */
exports.ingest = async (req, res) => {
  const documentId = randomUUID();

  try {
    const extracted = await sendToOCR(req.file);
    store.save(documentId, extracted);
  } catch {
    store.save(documentId, {});
  }

  res.json({ document_id: documentId });
};

/**
 * Single document verification
 */
exports.verifySingle = (req, res) => {
  const { document_id, policy_id } = req.body;

  const policy = policies[policy_id];
  if (!policy) {
    return res.status(400).json({
      error: `Invalid policy_id: ${policy_id}`
    });
  }

  const data = store.get(document_id) || {};
  const results = verify(data, policy);

  res.json({ document_id, results });
};


/**
 * Batch verification
 */
exports.verifyBatch = (req, res) => {
  const { document_ids, policy_id } = req.body;

  const policy = policies[policy_id];
  if (!policy) {
    return res.status(400).json({
      error: `Invalid policy_id: ${policy_id}`
    });
  }

  const candidates = document_ids.map((id) => {
    const data = store.get(id) || {};
    const results = verify(data, policy);

    const fields = {};
    let overall = "VERIFIED";

    for (const f of policy.required_fields) {
      fields[f] = results[f]?.status || "MISSING";
      if (fields[f] === "MISSING") overall = "MISSING";
      else if (fields[f] === "FLAGGED" && overall !== "MISSING")
        overall = "FLAGGED";
    }

    return { document_id: id, overall_status: overall, fields };
  });

  res.json({ candidates });
};


/*
This prototype processes documents synchronously and can be extended
to async batch pipelines and persistent storage in production.
*/
