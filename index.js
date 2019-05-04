const express = require("express");
const multer = require("multer");
const path = require("path");
let fs = require("fs");
let PDFParser = require("pdf2json");
const app = express();
const port = process.env.PORT || 3003;

//multer setting
var storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, "./public/myuploads");
  },
  filename: function(req, file, cb) {
    cb(null, file.fieldname + ".pdf");
  }
});

var upload = multer({
  storage: storage
}).single("pdffile");

app.get("/", function(req, res) {
  res.sendFile(__dirname + "/index.html");
});

//set static folder
app.use(express.static("."));
app.use(express.static("./public"));

//description of routes

app.post("/upload", (req, res) => {
  upload(req, res, error => {
    if (error) {
      return res.end("Error uploading file.");
    } else {
      let pdfParser = new PDFParser(this, 1);
      pdfParser.on("pdfParser_dataError", errData => console.error(errData));
      pdfParser.on("pdfParser_dataReady", pdfData => {
        fs.writeFileSync("./sample.txt", pdfParser.getRawTextContent());
      });
      pdfParser.loadPDF(
        path.resolve(__dirname + "/public/myuploads/pdffile.pdf")
      );
      res.end("File is uploaded", {
        filename: `myuploads/${req.file.filename}`
      });
    }
  });
});
app.listen(port, () => console.log(`server is running fine at ${port}...`));
