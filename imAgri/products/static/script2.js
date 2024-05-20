function register(event) {
  event.preventDefault();
  const formData = new FormData(document.getElementById("signup-form"));
  const data = {
    name: formData.get("companyName"),
    email: formData.get("email"),
    phone_number: formData.get("phone_number"),
    password: formData.get("password"),
    website: formData.get("website"),
    location: formData.get("location"),
    address: formData.get("address")
  };

  fetch("/organizations/register/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Registration Success:", data);
      window.location.href = "http://127.0.0.1:8000/organizations/login/";
    })
    .catch((error) => console.error("Registration Error:", error));
}

async function login(event) {
  event.preventDefault();
  const formData = new FormData(document.getElementById("login-form"));
  const data = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
  
    const responseData = await response.json();
    console.log("Login Success:", responseData);
    
    localStorage.setItem("token", responseData.token);
    localStorage.setItem("user", JSON.stringify(responseData.user));
    updateNavbarForLoggedInUser();
  } catch (error) {
    console.error("Login Error:", error);
  }
}

function updateNavbarForLoggedInUser() {
  const navbarLinks = document.querySelector(".navbar-links");
  navbarLinks.innerHTML = "";
  navbarLinks.innerHTML = `
        <a href='/add-product.html/' class="btn btn-add-product">Add Product</a>
        
    `;

  document
    .querySelector(".btn-add-product")
    .addEventListener("click", addProduct);
  
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");

  // const navbarLinks = document.querySelector(".navbar-links");
  // navbarLinks.innerHTML = `
  //       <button class="btn btn-signup">Sign Up</button>
  //       <button class="btn btn-signin">Sign In</button>
  //   `;

  window.location.href = "http://127.0.0.1:8000/";
}
document.querySelector(".btn-logout").addEventListener("click", logout);
function addProduct(event) {
  event.preventDefault();
 
  const formData = new FormData(document.getElementById("add-product-form"));
  const productData = {
    disease: formData.get("disease"),
    name: formData.get("name"),
    link: formData.get("link"),
  };

  console.log(productData);

  if (productData.disease === "Select Disease") {
    alert("Please select a valid disease.");
    return;
  }

  fetch("/organizations/products/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
    body: JSON.stringify(productData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok: " + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      console.log("Product added successfully:", data);
      alert("Product added successfully!");
    })
    .catch((error) => {
      console.error("Error adding product:", error);
      alert("Failed to add product: " + error.message);
    });
}

function displayImage(event) {
  const image = document.getElementById("selectedImage");
  const addImageText = document.getElementById("addImageText");

  if (event.target.files[0]) {
    const reader = new FileReader();
    reader.onload = (e) => {
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
  const resultsDiv = document.getElementById("results");

  resultsDiv.innerHTML = `
      <div class='result-label'>Results</div>
      <div class='result'>Disease: ${data.disease} <br> Prediction: ${
    data.prediction
  } <br> Confidence: ${data.confidence}%</div>
      <div class='result'>Preventive Measures: ${data[
        "Preventive Measures"
      ].join(", ")}</div>
      <div class='result'>Treatment Options: ${data["Treatment Options"].join(
        ", "
      )}</div>
      <div class='result'>Links: ${data.Links.join(", ")}</div>
    `;

  resultsDiv.style.display = "block";
}

document.addEventListener("DOMContentLoaded", function () {
  const pathname = window.location.pathname;
  if (pathname === "/index.html" || pathname === "/") {
    initializeIndexPage();
  }
});

function initializeIndexPage() {
  const submitButton = document.getElementById("submitButton");
  if (submitButton) {
    submitButton.addEventListener("click", async function () {
      const imageInput = document.getElementById("imageInput");
      const file = imageInput.files[0];
      const resultsDiv = document.getElementById("results");
      document.querySelector(".right-column").style.display = "none";
      document.querySelector(".loader-box").style.display = "flex";

      try {
        const formData = new FormData();
        formData.append("image", file);
        const response = await fetch("/make-prediction", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) throw new Error("Failed to fetch prediction");
        const data = await response.json();
        showResults(data);
      } catch (error) {
        console.error(error);
        resultsDiv.innerHTML =
          "<div class='result-label'>Error</div><div class='result'>Failed to fetch prediction</div>";
        resultsDiv.style.display = "block";
        document.querySelector(".loader-box").style.display = "none";
      }
    });
  }

  const mockData = {
    disease: "Example Disease",
    prediction: "Example Prediction",
    confidence: 80,
    "Preventive Measures": ["Measure 1", "Measure 2", "Measure 3"],
    "Treatment Options": ["Option 1", "Option 2", "Option 3"],
    Links: ["Link 1", "Link 2", "Link 3"],
  };

  showResults(mockData);
}
