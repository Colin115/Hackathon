// video
var video = document.getElementById("videoElement");
var captureButton = document.getElementById("captureButton");
var retakeButton = document.getElementById("retakeButton");
var submitButton = document.getElementById("submitButton");
var capturedImage = document.getElementById("capturedImage");
const constraints = {
  video: {
    width: { min: 1280 }, // Specify minimum width for higher quality
    height: { min: 720 }, // Specify minimum height for higher quality
  },
};
// Access the user's camera
navigator.mediaDevices
  .getUserMedia(constraints)
  .then(function (stream) {
    video.srcObject = stream;
  })
  .catch(function (error) {
    console.error("Error accessing the camera:", error);
  });

// Function to capture a frame from the video stream
function captureFrame(event) {
  event.preventDefault();
  var canvas = document.createElement("canvas");
  var context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  capturedImage.src = canvas.toDataURL("image/png");
  capturedImage.style.display = "block"; // display image
  video.style.display = "none"; // Hide the video element

  captureButton.setAttribute("disabled", "disabled");
  retakeButton.removeAttribute("disabled");
  submitButton.removeAttribute("disabled");
}

function retakePhoto(event) {
  event.preventDefault();
  capturedImage.style.display = "none"; // display image
  video.style.display = "block"; // Hide the video element

  captureButton.removeAttribute("disabled", "disabled");
  retakeButton.setAttribute("disabled", "disabled");
  submitButton.setAttribute("disabled", "disabled");
}
///

function submitVerifyID(event) {
  event.preventDefault();
  var imageData = dataURItoBlob(capturedImage.src);

  const formData = new FormData();
  formData.append(
    "front",
    document.getElementById("licenseInputFront").files[0]
  );
  formData.append("back", document.getElementById("licenseInputBack").files[0]);
  formData.append("selfie", imageData);
  // Send the form data to the server
  fetch("/api/verify_user_id/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success === false) {
        alert("Error verifying");
      } else {
        window.location.href = data.url;
      }
    });
}

function dataURItoBlob(dataURI) {
  // Convert base64 to raw binary data held in a string
  var byteString = atob(dataURI.split(",")[1]);

  // Separate the mime component
  var mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];

  // Write the bytes of the string to an ArrayBuffer
  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }

  // Create a Blob from the ArrayBuffer
  return new Blob([ab], { type: mimeString });
}

function displayFileName(inputId) {
  const fileInput = document.getElementById(inputId);
  const fileNameSpan = fileInput.parentElement.querySelector(".file-name");

  if (fileInput.files.length > 0) {
    fileNameSpan.textContent = fileInput.files[0].name;
  } else {
    fileNameSpan.textContent = "";
  }
}
