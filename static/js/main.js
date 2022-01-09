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
  if (document.getElementById("stateName").value == "Select") {
    document.getElementById("results").innerHTML = "Select a State";
    return;
  }
  if (body.district == "Select") {
    document.getElementById("results").innerHTML = "Select a Ditrict";
    return;
  }
  if (body.season == "Select") {
    document.getElementById("results").innerHTML = "Select a Season ";
    return;
  }
  if (body.year == "") {
    document.getElementById("results").innerHTML = "Fill a Year ";
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
    .then((res) => {
      if (!res.ok) throw "response staus is not ok " + res.status;
      return res.json();
    })
    .then((data) => {
      let crops = data.result;
      let htmlString = "<table><tr><th>Crop</th><th>Yield</th></tr>";
      for (let i = 0; i < crops.length; i++) {
        htmlString +=
          "<tr><td>" +
          crops[i][0] +
          "</td><td>" +
          crops[i][1].toFixed(2) +
          "</td></tr>";
      }
      htmlString += "</table>";
      document.getElementById("results").innerHTML = htmlString;
      return;
    })
    .catch((error) => {
      console.log("error while prediction " + error.data);
      document.getElementById("results").innerHTML =
        "Something Went Wrong 🤕🤕🤕";
    });
}
document.getElementById("districtName").innerHTML =
  "<option value='Select'>Select A State</option>";
function List2PicklistValue(list) {
  result = "<option value='Select'>Select</option>";
  for (idx in list) {
    result += "<option value='" + list[idx] + "'>" + list[idx] + "</option>\n";
  }
  return result;
}

function stateSelected() {
  let state = document.getElementById("stateName").value;
  if (state == "Select") {
    document.getElementById("districtName").innerHTML =
      "<option value='Select'>Select A State</option>";
  } else {
    document.getElementById("districtName").innerHTML = List2PicklistValue(
      stateDistrictMap[state]
    );
  }
}
