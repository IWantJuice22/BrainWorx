const burgerIcon = document.querySelector("#burger");
const navbarMenu = document.querySelector("#nav-links");

//const notification = document.querySelector('#notification');
var notificationClose = document.getElementById("notification_close");
let imagesDict = {};
let imagesLimit = 3;

burgerIcon.addEventListener("click", () => {
  navbarMenu.classList.toggle("is-active");
});

document.addEventListener("DOMContentLoaded", () => {
  (document.querySelectorAll(".notification .delete") || []).forEach(
    ($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    }
  );
});

function addImageInput(amount) {
  let imageLimit = 3;
  if (imageLimit - (amount + 1) == -1) {
    alert(
      "The maximum number of images is 3. To add another image, please remove an existing one."
    );
    return;
  }

  addImageButton = document.createElement("button");
  addImageButton.id = "addImageButton";
  addImageButton.type = "button";
  addImageButton.setAttribute(
    "onclick",
    "addImageInput(" + (Number(amount) + 1).toString() + ")"
  );
  addImageButton.classList.add("button");
  addImageButton.classList.add("is-primary");
  addImageButton.classList.add("is-outlined");

  buttonText = document.createTextNode(
    "Add Image (" + (imageLimit - (Number(amount) + 1)).toString() + " left) "
  );

  addImageButton.appendChild(buttonText);
  const addImagesHere = document.getElementById("addImagesHere");

  const imageInputDiv = document.createElement("div");
  imageInputDiv.id = "imageInputDiv";
  imageInputDiv.classList.add("control");
  imageInputDiv.classList.add("column");
  const imageInput = document.createElement("input");
  imageInput.id = "imageInput";
  imageInput.classList.add("button");
  imageInput.classList.add("is-size-7");
  imageInput.classList.add("is-outlined");
  imageInput.classList.add("is-info");
  imageInput.type = "file";
  imageInput.accept =
    "image/png, image/jpeg, image/gif, image/ico, image/jpg, image/heic";
  imageInput.hidden = true;
  document.getElementById("addImageButton").remove();
  imageInputDiv.appendChild(imageInput);
  addImagesHere.appendChild(imageInputDiv);

  imageInput.addEventListener("change", function (e) {
    const reader = new FileReader();
    reader.onload = function () {
      const img = new Image();

      img.src = reader.result;

      imgX = Number(img.width);
      imgY = Number(img.height);

      if (imgX == 0) {
        imgX += 400;
        imgY += 400;
      }
      if (imgY < 100) {
        imgY += 100;
      }
      while (imgY > 200) {
        imgY = imgY / 2;
        imgX = imgX / 2;
      }
      img.width = imgX.toString();
      img.height = imgY.toString();
      img.style.backgroundColor = "white";

      const imageColumnDiv = document.createElement("div");
      imageColumnDiv.classList.add("column");
      img.id = "daIMG";
      imageColumnDiv.appendChild(img);

      document.getElementById("displayImagesHere").appendChild(imageColumnDiv);
      if (imageLimit - (amount + 1) != 0) {
        document.getElementById("addButtonHere").appendChild(addImageButton);
      }
      document.getElementById("imageInput").remove();
      fakeTextField = document.createElement("input");
      fakeTextField.type = "text";

      fakeTextField.hidden = true;
      fakeTextField.name = "image" + (amount + 1);

      fakeTextField.value = encodeURI(reader.result);

      fakeTextField.id = "image" + (amount + 1);
      imageColumnDiv.appendChild(fakeTextField);
    };
    reader.readAsDataURL(imageInput.files[0]);
  });
}

function reduce(number, denomin) {
  var gcd = function gcd(a, b) {
    return b ? gcd(b, a % b) : a;
  };
  gcd = gcd(number, denomin);
  return [number / gcd, denomin / gcd];
}

function getDataUrl(img) {
  // Create canvas
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  // Set width and height
  canvas.width = img.width;
  canvas.height = img.height;
  // Draw the image
  ctx.drawImage(img, 0, 0);

  return canvas.toDataURL("image/jpeg");
}
