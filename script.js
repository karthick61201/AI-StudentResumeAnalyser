document.addEventListener("DOMContentLoaded", () => {

  const dropArea = document.getElementById("uploadArea");
  const fileInput = document.getElementById("fileInput");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const fileInfo = document.getElementById("fileInfo");
  const fileName = document.getElementById("fileName");

  let selectedFile = null;

  /* CLICK → OPEN FILE PICKER */
  dropArea.addEventListener("click", () => {
    fileInput.click();
  });

  /* FILE SELECT */
  fileInput.addEventListener("change", () => {
    selectedFile = fileInput.files[0];
    showFile(selectedFile);
  });

  /* DRAG OVER */
  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("active");
  });

  /* DRAG LEAVE */
  dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
  });

  /* DROP FILE */
  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("active");

    selectedFile = e.dataTransfer.files[0];
    showFile(selectedFile);
  });

  /* SHOW SELECTED FILE */
  function showFile(file) {
    if (!file) return;

    fileName.innerText = file.name;
    fileInfo.style.display = "flex";
    analyzeBtn.style.display = "inline-block";
  }

  /* REMOVE FILE */
  window.clearFile = function () {
    selectedFile = null;
    fileInput.value = "";
    fileInfo.style.display = "none";
    analyzeBtn.style.display = "none";
  };

  /* ANALYZE BUTTON */
  analyzeBtn.addEventListener("click", uploadResume);

  function uploadResume() {
    if (!selectedFile) {
      alert("Resume select pannu da 😅");
      return;
    }

    // UI before request
    document.getElementById("loadingSpinner").style.display = "block";
    document.getElementById("resultsSection").style.display = "none";
    document.getElementById("errorMessage").style.display = "none";

    const formData = new FormData();
    formData.append("resume", selectedFile);

    fetch("http://localhost:8000/api/upload", {
  method: "POST",
  body: formData
})





      .then(res => {
        if (!res.ok) {
          throw new Error("Backend response error");
        }
        return res.json();
      })
      .then(data => {
        console.log(data); // debug

        // Hide spinner
        document.getElementById("loadingSpinner").style.display = "none";

        // Show results
        document.getElementById("resultsSection").style.display = "block";

        /* 🔵 OVERALL SCORE */
        document.getElementById("overallScore").innerText =
          data.overall_score;

        /* 🟣 CATEGORY SCORES */

        // Formatting
        document.getElementById("formattingScore").innerText =
          data.category_scores.formatting + "%";
        document.getElementById("formattingProgress").style.width =
          data.category_scores.formatting + "%";

        // Content
        document.getElementById("contentScore").innerText =
          data.category_scores.content + "%";
        document.getElementById("contentProgress").style.width =
          data.category_scores.content + "%";

        // Experience
        document.getElementById("experienceScore").innerText =
          data.category_scores.experience + "%";
        document.getElementById("experienceProgress").style.width =
          data.category_scores.experience + "%";

        // Skills
        document.getElementById("skillsScore").innerText =
          data.category_scores.skills + "%";
        document.getElementById("skillsProgress").style.width =
          data.category_scores.skills + "%";

        /* 📋 EXTRACTED INFO */
        document.getElementById("emailExtracted").innerText =
          data.parsed_data.contact_info.email || "N/A";

        document.getElementById("phoneExtracted").innerText =
          data.parsed_data.contact_info.phone || "N/A";

      })
      .catch(err => {
        document.getElementById("loadingSpinner").style.display = "none";
        document.getElementById("errorMessage").style.display = "block";
        document.getElementById("errorText").innerText = err.message;
        console.error(err);
      });
  }

});
