const form = document.getElementById("predictionForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultDiv.style.display = "none";

  const data = {
    Pregnancies: +Pregnancies.value,
    Glucose: +Glucose.value,
    BloodPressure: +BloodPressure.value,
    SkinThickness: +SkinThickness.value,
    Insulin: +Insulin.value,
    BMI: +BMI.value,
    DiabetesPedigreeFunction: +DiabetesPedigreeFunction.value,
    Age: +Age.value,
  };

  // Frontend validation
  for (let key in data) {
    if (data[key] < 0) {
      showError("Invalid input: values must be non-negative.");
      return;
    }
    if (
      [
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "Age",
      ].includes(key) &&
      data[key] === 0
    ) {
      showError(`${key} cannot be zero.`);
      return;
    }
  }

  try {
    const response = await fetch(
      "https://diabetes-risk-prediction-qtad.onrender.com/predict",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }
    );

    if (!response.ok) {
      const err = await response.json();
      showError(err.detail || "Prediction failed.");
      return;
    }

    const result = await response.json();

    resultDiv.className = "message success";
    resultDiv.innerHTML = `
            Decision Tree: ${result.decision_tree_prediction}<br>
            Logistic Regression: ${result.logistic_regression_prediction}
        `;
    resultDiv.style.display = "block";
  } catch {
    showError("Unable to connect to backend.");
  }
});

function showError(msg) {
  resultDiv.className = "message error";
  resultDiv.textContent = msg;
  resultDiv.style.display = "block";
}
