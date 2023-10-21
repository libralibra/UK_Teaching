// check image alt and title strings, Daniel

// Get all the images in the document
// Get all the image elements in the document
var images = document.getElementsByTagName("img");

// Loop through each image element
for (var i = 0; i < images.length; i++) {
    // Get the current image element
    var image = images[i];

    // Get the alt and title attributes of the image
    var alt = image.getAttribute("alt");
    var title = image.getAttribute("title");

    // If alt is set and title is not, copy alt to title
    if (alt && !title) {
        image.setAttribute("title", alt);
    }

    // If title is set and alt is not, copy title to alt
    if (title && !alt) {
        image.setAttribute("alt", title);
    }
}
