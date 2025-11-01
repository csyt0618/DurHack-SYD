document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");
  const message = document.getElementById("error-message");

  if (form) {
    form.addEventListener("submit", async function (event) {
      event.preventDefault(); // stop reload

      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();

      try {
        const response = await fetch("/users");
        const data = await response.json();

        const users = data.user;
        const passwords = data.password;

        const userIndex = users.indexOf(username);

        if (userIndex !== -1 && passwords[userIndex] === password) {
          message.textContent = "✅ Login successful!";
          message.style.color = "green";

          // redirect to /home
          setTimeout(() => {
            window.location.href = "/home";
          }, 1000);
        } else {
          message.textContent = "❌ Invalid username or password.";
          message.style.color = "red";
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
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
