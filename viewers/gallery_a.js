

// Get the modal
var modal = document.getElementById("imageDetailPopUp");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var modalImg = document.getElementById("imgInPopup");
var captionText = document.getElementById("caption");


// Get the <span> element that closes the modal
var span = document.getElementsByClassName("closeImagePopUp")[0];
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    closeModal();
}



modal.onclick = function() {    
     closeModal();
}
  


function openImage(obj) {
    modal.style.display = "block";
    modalImg.src = obj.src;
    captionText.innerHTML = obj.alt;

    modalImg.onclick = function(event) {
        window.open(modalImg.src,"_blank");
        event.stopPropagation();
    }
    
    

}


function closeModal() {
    modal.style.display = "none";    
}
  
