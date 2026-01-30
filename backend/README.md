## AuthDoc- Backend File structure of the prototype
AuthDoc/
├── backend/
│   ├── node/
│   │   ├── package.json
│   │   ├── nodemon.json
│   │   ├── uploads/
│   │   └── src/
│   │       ├── app.js
│   │       ├── server.js
│   │       ├── config/
│   │       │   └── policies.json
│   │       ├── middleware/
│   │       │   └── upload.middleware.js
│   │       ├── routes/
│   │       │   └── verify.routes.js
│   │       ├── controllers/
│   │       │   └── verify.controller.js
│   │       ├── services/
│   │       │   ├── pythonClient.js
│   │       │   └── verifier.service.js
│   │       ├── store/
│   │       │   └── documentStore.js
│   │       └── utils/
│   │           └── status.util.js
│   │
│   └── python/
│       ├── main.py
│       ├── extractor.py
│       └── requirements.txt
│
└── README.md

 # workflow of the AuthDoc:
 Frontend
   |
   |  (file upload)
   v
Node.js (Express)  ───────────────►  Python (FastAPI)
   |                                      |
   |  verification + policies             |  OCR + extraction
   |                                      |
   |◄──────── extracted JSON ─────────────|
# Service Sturcture of the ML(python-FastAPI):
ocr_service/
├── main.py
├── extractor.py
├── requirements.txt
   ## Requirements:
      fastapi
      uvicorn
      paddleocr
      paddlepaddle
      python-multipart
      opencv-python
