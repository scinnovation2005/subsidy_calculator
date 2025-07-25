import { renderForm as renderMP } from './madhyapradesh.js';
import { renderForm as renderUPMSME } from './uttarpradesh_msme.js';
import { renderForm as renderUP } from './uttarpradesh.js';
import { renderForm as renderPunjab } from './punjab.js';
import { renderForm as renderHaryana } from './haryana.js';
import { renderForm as renderTamilnadu } from './tamilnadu.js';
import { renderForm as renderKarnataka } from './karnataka.js';
import { renderForm as renderRajasthan } from './rajasthan.js';
import { renderForm as renderMaharashtra } from './maharashtra.js';
import { renderForm as renderGujarat } from './gujarat.js';

const stateSelect = document.querySelector("#state");
const stateFormArea = document.querySelector("#stateFormArea");
const form = document.querySelector("#subsidyForm");
const statusDiv = document.querySelector("#status");

function getSelectedEnterpriseSize() {
  return document.querySelector("#enterpriseSize").value;
}

stateSelect.addEventListener("change", () => {
  const state = stateSelect.value;
  console.log('State: ', state)
  const size = getSelectedEnterpriseSize();
  stateFormArea.innerHTML = "";

  if (state === "Madhya Pradesh") {
    renderMP(stateFormArea);
  } 
  else if (state === "Uttar Pradesh") {
    const largeSizes = ["Large", "Mega", "Ultra Mega", "Super Mega"];
    if (largeSizes.includes(size)) {
      renderUP(stateFormArea);
    } else {
      renderUPMSME(stateFormArea);
    }
  }
  else if (state === "Punjab"){
    renderPunjab(stateFormArea);
  }
  else if (state === "Haryana"){
    renderHaryana(stateFormArea);
  }
  else if (state === "Tamil Nadu"){
    renderTamilnadu(stateFormArea);
  }
  else if (state === "Karnataka"){
    renderKarnataka(stateFormArea);
  }
   else if (state === "Maharashtra"){
    renderMaharashtra(stateFormArea);
  }
  else if (state === "Rajasthan"){
    renderRajasthan(stateFormArea);
  }
  else if ( state === "Gujarat"){
    renderGujarat(stateFormArea);
  }
});

document.querySelector("#enterpriseSize").addEventListener("change", () => {
  if (stateSelect.value === "Uttarpradesh") {
    stateSelect.dispatchEvent(new Event("change"));
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const progressContainer = document.querySelector("#progressContainer");
  const progressBar = document.querySelector("#progressBar");

  // Show the progress bar
  progressContainer.style.display = "block";
  progressBar.value = 0;

  // Simulate progress incrementally
  let progress = 0;
  const interval = setInterval(() => {
    progress = Math.min(progress + Math.random() * 10, 90); // random progress till 90%
    progressBar.value = progress;
  }, 300);


  const formData = new FormData(form);
  const data = {};
  for (let [key, value] of formData.entries()) {
    if (value !== "") data[key] = value;
  }

  console.log("Collected form data:", data);

  try {
    console.log('Calling the api')
    const response = await fetch("https://subsidy-calculator-1.onrender.com/subsidy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    
    console.log("Raw response:", response);
    const result = await response.json();
    console.log("Result from API:", result); 

    if (result.report_path) {
      const filename = result.report_path.split("/").pop();
      const downloadUrl = `https://subsidy-calculator-1.onrender.com/download_pdf/${filename}`;
      
      clearInterval(interval);
      progressBar.value = 100;

      setTimeout(() => {
        progressContainer.style.display = "none";
        statusDiv.innerHTML = `Report generated. <a href="${downloadUrl}" target="_blank" download>Click to download PDF</a>`;
      }, 500); // small delay to show 100% progress

    } else {
      progressContainer.style.display = "none";
      statusDiv.innerHTML = `Error: ${result.error || "Unknown error"}`;
    }
  } catch (err) {
      clearInterval(interval);
      progressContainer.style.display = "none";
      console.error(err);
      statusDiv.innerHTML = "Something went wrong while generating the report.";
  }
  
});

// === Industry Type: Show/Hide "Other" Input ===
  const industryTypeSelect = document.querySelector("#industryType");
  const otherIndustryContainer = document.querySelector("#otherIndustryContainer");
  const otherIndustryInput = document.querySelector("#otherIndustry");

  function toggleOtherInput() {
    const selected = industryTypeSelect.value;
    if (selected === "Other") {
      otherIndustryContainer.classList.add("show");
      otherIndustryInput.required = true;
    } else {
      otherIndustryContainer.classList.remove("show");
      otherIndustryInput.value = "";
      otherIndustryInput.required = false;
    }
  }

  // Attach event listener
  industryTypeSelect.addEventListener("change", toggleOtherInput);
