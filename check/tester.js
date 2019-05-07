let CopyleaksCloud = require("plagiarism-checker");
let _ = require("lodash");
const fs = require("fs");
let clCloud = new CopyleaksCloud();
let config = clCloud.getConfig();

let email = "sajalgarg17.sg@gmail.com";
let apikey = "84B4948A-7080-4748-8454-7844D27B1C58";

function getStatus(_pid, cb) {
  clCloud.getProcessStatus(_pid, function(resp, err) {
    cb(resp);
    console.log(resp);

    if (!isNaN(err)) console.log("error: " + err);
  });
}

function init(pid, cb) {
  const timer = setInterval(() => {
    getStatus(pid, resp => {
      if (resp.Status === "Finished") {
        clearInterval(timer);
        cb();
      }
    });
  }, 1000);
}

function abc(done) {
  clCloud.login(email, apikey, config.E_PRODUCT.Education, callback);

  function callback(resp, err) {
    let _customHeaders = {};

    let _file = process.cwd() + "/check/files/search.txt";
    clCloud.createByFile(_file, _customHeaders, function(resp, err) {
      if (resp && resp.ProcessId) {
        init(resp.ProcessId, () => {
          clCloud.getProcessResults(resp.ProcessId, function(resp, err) {
            console.log(resp);
            const res = resp.map(curr => {
              return {
                match_url: curr.URL,
                match_percents: curr.Percents,
                Number_of_copied_words: curr.NumberOfCopiedWords
              };
            });
            fs.writeFileSync("./output.json", JSON.stringify(res, null, 2));
            if (isNaN(err)) console.log("error: " + err);
            done();
          });
        });
        console.log("Process has been created--> " + resp.ProcessId);
      }
      if (!isNaN(err)) {
        console.log("error: " + err);
        done(err);
      }
    });
  }
}

process.on("exit", function() {
  console.log("Process closed !!");
});
module.exports = {
  abc
};
