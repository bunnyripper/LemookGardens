const menuToggle=document.querySelector(".menu-toggle");
const navlinks=document.querySelector(".nav-links");

menuToggle.addEventListener("click", ()=> {
    navlinks.classList.toggle("is-open");

    const isOpen = navlinks.classList.contains("is-open");
    menuToggle.setAttribute("aria-expanded",isOpen);
});


document.addEventListener("DOMContentLoaded", () => {

    const diningSlides = document.querySelectorAll(".dining-slide");

    if (diningSlides.length > 1) {

        let currentSlide = 0;

        setInterval(() => {

            diningSlides[currentSlide].classList.remove("active");

            currentSlide = (currentSlide + 1) % diningSlides.length;

            diningSlides[currentSlide].classList.add("active");

        }, 2000);

    }

});

const eventOptions = document.querySelectorAll(".event-option");
const eventImages = document.querySelectorAll(".event-image");

eventOptions.forEach(option => {

    const changeEventImage = () => {

        const target = option.dataset.event;

        eventOptions.forEach(item => {
            item.classList.remove("active");
        });

        option.classList.add("active");

        eventImages.forEach(img => {
            img.classList.remove("active");

            if (img.dataset.event === target) {
                img.classList.add("active");
            }
        });

    };

    option.addEventListener("mouseenter", changeEventImage);
    option.addEventListener("click", changeEventImage);

});

/* ========================================
   GALLERY LIGHTBOX
======================================== */

const galleryItems = document.querySelectorAll(".gallery-item");
const lightbox = document.getElementById("gallery-lightbox");
const lightboxImage = document.getElementById("lightbox-image");
const lightboxCounter = document.getElementById("lightbox-counter");

const lightboxClose = document.getElementById("lightbox-close");
const lightboxPrev = document.getElementById("lightbox-prev");
const lightboxNext = document.getElementById("lightbox-next");

let currentImage = 0;


/* Open image */

function openLightbox(index){

    currentImage = index;

    const image = galleryItems[currentImage].querySelector("img");

    lightboxImage.src = image.src;
    lightboxImage.alt = image.alt;

    lightboxCounter.textContent =
        `${currentImage + 1} / ${galleryItems.length}`;

    lightbox.classList.add("active");
    lightbox.setAttribute("aria-hidden", "false");

    document.body.style.overflow = "hidden";
}


/* Close image */

function closeLightbox(){

    lightbox.classList.remove("active");
    lightbox.setAttribute("aria-hidden", "true");

    document.body.style.overflow = "";
}


/* Previous */

function showPrevious(){

    currentImage =
        (currentImage - 1 + galleryItems.length)
        % galleryItems.length;

    openLightbox(currentImage);
}


/* Next */

function showNext(){

    currentImage =
        (currentImage + 1)
        % galleryItems.length;

    openLightbox(currentImage);
}


/* Click gallery photos */

galleryItems.forEach((item, index) => {

    item.addEventListener("click", () => {
        openLightbox(index);
    });

});


/* Buttons */

lightboxClose.addEventListener("click", closeLightbox);

lightboxPrev.addEventListener("click", showPrevious);

lightboxNext.addEventListener("click", showNext);


/* Close when clicking the dark background */

lightbox.addEventListener("click", (event) => {

    if(event.target === lightbox){
        closeLightbox();
    }

});


/* Keyboard controls */

document.addEventListener("keydown", (event) => {

    if(!lightbox.classList.contains("active")){
        return;
    }

    if(event.key === "Escape"){
        closeLightbox();
    }

    if(event.key === "ArrowLeft"){
        showPrevious();
    }

    if(event.key === "ArrowRight"){
        showNext();
    }

});