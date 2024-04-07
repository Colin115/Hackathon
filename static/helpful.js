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
