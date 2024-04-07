const profileLink = document.getElementById("profileLink");

function getProfileLink() {
  fetch("/api/get_profile_link/", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      profileLink.setAttribute("href", data.url);
    });
}

window.onload = getProfileLink;

function logout(event) {
  event.preventDefault();

  fetch("/api/logout", {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      alert("Successfully logged out");
      window.location.href = "/";
    });
}
