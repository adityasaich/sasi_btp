let stateDistrictMap;
fetch(new URL(document.URL) + "/stateDistrictMap")
  .then((res) => res.json())
  .then((data) => {
    stateDistrictMap = data["result"];
    document.getElementById("stateName").innerHTML = List2PicklistValue(
      Object.keys(stateDistrictMap)
    );
  })
  .catch((error) => {
    console.log("error getting states and districts from server :(");
  });
fetch(new URL(document.URL) + "options?param=Season")
  .then((res) => res.json())
  .then((data) => (document.getElementById("season").innerHTML = data.result))
  .catch((error) => {
    console.log("error getting seasons from server :(");
  });
fetch(new URL(document.URL) + "options?param=Crop")
  .then((res) => res.json())
  .then((data) => (document.getElementById("crop").innerHTML = data.result))
  .catch((error) => {
    console.log("error getting crops from server :(");
  });
function predict() {
  document.getElementById("results").innerHTML = "Fetching Data ⏳⏳⏳";
  let body = {
    district: document.getElementById("districtName").value,
    season: document.getElementById("season").value,
    year: document.getElementById("year").value,
    crop: document.getElementById("crop").value,
  };
  if (!body.district || !body.season || !body.year || !body.crop) {
    document.getElementById("results").innerHTML =
      "Select a State,District,Crop and Season";
    return;
  }
  fetch(new URL(document.URL) + "predict", {
    method: "POST",
    mode: "same-origin",
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(body), // body data type must match "Content-Type" header
  })
    .then((res) => res.json())
    .then((data) => {
      let crops = data.result;
      let htmlString = "";
      for (let i = 0; i < crops.length; i++) {
        htmlString += "<p><h2>" + crops[i][0] + " " + crops[i][1] + "</h2></p>";
      }
      document.getElementById("results").innerHTML = htmlString;
      return;
    })
    .catch((error) => {
      console.log("error while prediction " + error.data);
      document.getElementById("results").innerHTML =
        "Something Went Wrong 🤕🤕🤕";
    });
}

function List2PicklistValue(list) {
  result = "";
  for (idx in list) {
    result += "<option value='" + list[idx] + "'>" + list[idx] + "</option>\n";
  }
  return result;
}

function stateSelected() {
  let state = document.getElementById("stateName").value;
  document.getElementById("districtName").innerHTML = List2PicklistValue(
    stateDistrictMap[state]
  );
}
