const express = require("express");
const multer = require("multer");
const path = require("path");
let fs = require("fs");
let PDFParser = require("pdf2json");
const app = express();
const port = process.env.PORT || 3003;
const router = express.Router();
var checkdata = require("./check/tester");

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

//set static folder
app.use(express.static("."));
app.use(express.static("./public"));

//routes

//@type - GET /home
//@desc - route to home page
//@access -   PUBLIC
app.get("/", function(req, res) {
  res.sendFile(__dirname + "/index.html");
});

//@type - POST /upload
//@desc - route to check page
//@access -   PUBLIC
app.post("/upload", (req, res) => {
  upload(req, res, error => {
    if (error) {
      return res.end("Error uploading file.");
    } else {
      let pdfParser = new PDFParser(this, 1);
      pdfParser.on("pdfParser_dataError", errData => console.error(errData));
      pdfParser.on("pdfParser_dataReady", pdfData => {
        fs.writeFileSync(
          "./check/files/search.txt",
          pdfParser.getRawTextContent()
        );
      });
      pdfParser.loadPDF(
        path.resolve(__dirname + "/public/myuploads/pdffile.pdf")
      );
      const spawn = require("child_process").spawn;
      const ls = spawn("python3", ["script.py"]);

      ls.stdout.on("data", data => {
        console.log(`stdout: ${data}`);
      });

      ls.stderr.on("data", data => {
        console.log(`stderr: ${data}`);
      });

      ls.on("close", code => {
        console.log(`child process exited with code ${code}`);
      });
      res.redirect("/check");
      res.end("ended");
    }
  });
});

//@type - POST /upload
//@desc - route to check page
//@access -   PUBLIC
app.use("/", router);
router.get("/check", function(req, res) {
  checkdata.abc();
  res.end("This is the check page");
});

module.exports = router;
app.listen(port, () => console.log(`server is running fine at ${port}...`));
