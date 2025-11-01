function validateForm() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let errorMessage = document.getElementById("error-message");

  let correctUsername = "student";
  let correctPassword = "12345";

  if (username === correctUsername && password === correctPassword) {
    alert("Login successful!");
    return true; // form will submit
  } else {
    errorMessage.textContent = "Invalid username or password!";
    return false; // stops form submission
  }
}


