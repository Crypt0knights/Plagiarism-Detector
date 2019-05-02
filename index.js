const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const pdf = require("pdf-parse");

const app = express();
const port = process.env.PORT || 3003;

//multer setting
var storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, "./public/myuploads");
  },
  filename: function(req, file, cb) {
    cb(
      null,
      file.fieldname + "-" + Date.now() + path.extname(file.originalname)
    );
  }
});

var upload = multer({
  storage: storage
}).single("pdffile");

app.get("/", function(req, res) {
  res.sendFile(__dirname + "/index.html");
});

app.use(express.static("."));
//set static folder
app.use(express.static("./public"));

//description
app.post("/upload", (req, res) => {
  upload(req, res, error => {
    if (error) {
      return res.end("Error uploading file.");
    } else {
      res.end("File is uploaded", {
        filename: `myuploads/${req.file.filename}`
      });
    }
  });
});
//extracting text from pdf file
/*let dataBuffer = fs.readFileSync("./public/myuploads/filename");
pdf(dataBuffer).then(function(data) {
  console.log(data.text);
});*/

app.listen(port, () => console.log(`server is running fine at ${port}...`));
