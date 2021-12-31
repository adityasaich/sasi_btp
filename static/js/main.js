fetch(new URL(document.URL) + "options?param=District_Name")
  .then((res) => res.json())
  .then(
    (data) => (document.getElementById("districtName").innerHTML = data.result)
  );
fetch(new URL(document.URL) + "options?param=Season")
  .then((res) => res.json())
  .then((data) => (document.getElementById("season").innerHTML = data.result));

function predict() {
  let body = {
    district: document.getElementById("districtName").value,
    season: document.getElementById("season").value,
    year: document.getElementById("year").value,
  };
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
        htmlString += "<p><h2>" + crops[i] + "</h2></p>";
      }
      document.getElementById("results").innerHTML = htmlString;
    });
}
