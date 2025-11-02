document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");
  const message = document.getElementById("error-message");

  if (form) {
    form.addEventListener("submit", async function (event) {
      event.preventDefault(); // stop reload

      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();

      try {
        const response = await fetch("/login_user", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        const result = await response.json();

        if (result.success) {
          message.textContent = "✅ Login successful!";
          message.style.color = "green";

          setTimeout(() => {
            window.location.href = "/home";
          }, 1000);
        } else {
          message.textContent = "❌ " + result.message;
          message.style.color = "red";
        }
      } catch (error) {
        console.error("Error logging in:", error);
        message.textContent = "⚠️ Server error.";
        message.style.color = "orange";
      }
    });
  }
});


// ----------------- REGISTER PAGE -----------------
async function registerUser() {
  const username = document.getElementById("newUsername").value.trim();
  const password = document.getElementById("newPassword").value.trim();
  const message = document.getElementById("registerMessage");

  try {
    const response = await fetch("/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    message.textContent = result.message;
    message.style.color = result.success ? "green" : "red";

    if (result.success) {
      setTimeout(() => {
        window.location.href = "/login";
      }, 1500);
    }
  } catch (error) {
    console.error("Registration error:", error);
    message.textContent = "⚠️ Could not register user.";
    message.style.color = "orange";
  }

  return false;
}

function goToLogin() {
  window.location.href = "/login";
}

function goHome() {
  window.location.href = "/";
}

/*only for home.html*/
document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.querySelector(".submitBtn");
  const paragraphBox = document.querySelector("textarea");
  const output = document.getElementById("dishOutput");

  if (!submitBtn || !paragraphBox) return; // not on home page

  submitBtn.addEventListener("click", async () => {
    const sliders = {
      stress: +document.getElementById("stressRange").value,
      happiness: +document.getElementById("happinessRange").value,
      energy: +document.getElementById("energyRange").value,
      sociability: +document.getElementById("sociabilityRange").value,
      appetite: +document.getElementById("appetiteRange").value,
      socialStress: +document.getElementById("socialStress").value,
      emotionalStress: +document.getElementById("emotionalStress").value,
      physicalStress: +document.getElementById("physicalStress").value,
      sadness: +document.getElementById("sadness").value,
      motivation: +document.getElementById("motivation").value,
      contentment: +document.getElementById("contentment").value,
      physicalFatigue: +document.getElementById("physicalFatigue").value,
      emotionalFatigue: +document.getElementById("emotionalFatigue").value,
      energetic: +document.getElementById("energetic").value,
      introverted: +document.getElementById("introverted").value,
      socialAnxious: +document.getElementById("socialAnxious").value,
      binging: +document.getElementById("binging").value,
      craving: document.getElementById("cravingSelect").value,
      timeOfDay: document.getElementById("timeSelect").value
    };

    const paragraph = paragraphBox.value.trim();
    const diet = document.getElementById("dietSelect").value;
    const allergens = document.getElementById("allergensInput").value.trim();
    output.textContent = "Thinking...";

    try {
      const resp = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sliders, paragraph, diet, allergens })
      });

      const data = await resp.json();

      if (!data.ok) {
        output.textContent = "Error: " + (data.error || "Unknown");
        return;
      }

      const r = data.result;
      output.innerHTML = `
        <p>🍽 Dish: ${r.dish}</p><br>
        <p>Why: ${r.reason}</p><br>
        <p>Ingredients:<br> - ${r.ingredients.join("<br> - ")}</p><br>
        <p>Suggestion: ${r.suggestion}</p>
      `;
    } catch (err) {
      output.textContent = "Network or server error: " + err;
    }
  });
});

