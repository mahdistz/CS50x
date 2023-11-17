const paragraphContainer = document.querySelector(".paragraph-container");
const readMoreLink = document.querySelector(".read-more");

readMoreLink.addEventListener("click", function() {
  paragraphContainer.classList.toggle("visible");
});