let CopyleaksCloud = require("plagiarism-checker");
let _ = require("lodash");
const fs = require("fs");
let clCloud = new CopyleaksCloud();
let config = clCloud.getConfig();

let email = "raushanbihari007@gmail.com";
let apikey = "439d16cc-bd28-453f-bb4b-09d498e5a036";

function getStatus(_pid, cb) {
  clCloud.getProcessStatus(_pid, function(resp, err) {
    cb(resp);
    console.log(resp);
    if (!isNaN(err)) console.log("Error: " + err);
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

(function() {
  clCloud.login(email, apikey, config.E_PRODUCT.Education, callback);

  function callback(resp, err) {
    let _customHeaders = {};

    let _file = process.cwd() + "/search.txt";
    clCloud.createByFile(_file, _customHeaders, function(resp, err) {
      if (resp && resp.ProcessId) {
        init(resp.ProcessId, () => {
          clCloud.getProcessResults(resp.ProcessId, function(resp, err) {
            console.log(resp);
            const res = resp.map(curr => {
              return {
                url: curr.URL,
                Percents: curr.Percents,
                NumberOfCopiedWords: curr.NumberOfCopiedWords
              };
            });
            fs.writeFileSync("./result.json", JSON.stringify(res, null, 2));
            if (isNaN(err)) console.log("Error: " + err);
          });
        });
        console.log("Process has been created: " + resp.ProcessId);
      }
      if (!isNaN(err)) console.log("Error: " + err);
    });
  }
})();

process.on("exit", function() {
  console.log("Closed process");
});
