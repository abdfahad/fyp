function displayImage(event) {
  var image = document.getElementById("selectedImage");
  var addImageText = document.getElementById("addImageText");
  if (event.target.files && event.target.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      image.src = e.target.result;
      image.style.display = "block";
      addImageText.style.display = "none";
    };
    reader.readAsDataURL(event.target.files[0]);
  }
}

function showResults(data) {
  document.querySelector(".loader-box").style.display = "none";
  document.querySelector(".right-column").style.display = "block";
  var resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = `
<div class='result-label'>Results</div>
<div class='result'>Predicted Disease: ${data.prediction} <br> Confidence: ${
    data.confidence
  }%</div>
<div class='result'>Preventive Measures: <br/>
    <ul>
    ${data["preventive_measures"].map((mes) => `<li>${mes}</li>`).join(" ")}
    </ul>
</div>
<div class='result'>Treatment Options:
<ul>
${data["treatment_options"].map((mes) => `<li>${mes}</li>`).join(" ")}
</ul>
<div class='result'>Links: 
<ul>
    ${data.links.map((mes) => `<li><a href=${mes}>${mes}</a></li>`).join(" ")}
</ul>
</div>
${
  data.products.length > 0
    ? `
    <div class="table-container">
    <table class="result-table">
      <thead>
        <tr>
      
          <th class='text-sm'>Product</th>
          <th class='text-sm'>Product Link</th>
          <th class='text-sm'>Org Name</th>
          <th class='text-sm'>Org Address</th>
          <th class='text-sm'>Org Email</th>
          <th class='text-sm'>Org Number</th>
          <th class='text-sm'>Org Website</th>
          <th class='text-sm'>Org Location</th>
        </tr>
      </thead>
      <tbody>
        ${data.products
          .map(
            (product) => `
          <tr class='text-sm'>
            
            <td >${product.product}</td>
            <td>${product.product_link}</td>
            <td>${product.org__name}</td>
            <td>${product.org__address}</td>
            <td>${product.org__email}</td>
            <td>${product.org__phone_number}</td>
            <td>${product.org__website}</td>
            <td>${product.org__location}</td>
          </tr>
        `
          )
          .join("")}
      </tbody>
    </table>
  </div>  
`
    : ""
}
`;


  resultsDiv.style.display = "block";
}

document
  .getElementById("submitButton")
  .addEventListener("click", async function () {
    const imageInput = document.getElementById("imageInput");
    const file = imageInput.files[0];

    console.log(file);
    var resultsDiv = document.getElementById("results");
    var treatmentDiv = document.getElementById("treatment");
    document.querySelector(".right-column").style.display = "none";
    document.querySelector(".loader-box").style.display = "flex";

    try {
      const formData = new FormData();
      formData.append("image", file);

      const response = await fetch("/make-prediction/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to fetch prediction");
      }
      const data = await response.json();
      console.log(data, "{data}");
      showResults(data);
    } catch (error) {
      console.error(error);

      document.querySelector(".loader-box").style.display = "none";
      resultsDiv.innerHTML =
        "<div class='result-label'>Error</div><div class='result'>Failed to fetch prediction</div>";
      resultsDiv.style.display = "block";
    }
  });
