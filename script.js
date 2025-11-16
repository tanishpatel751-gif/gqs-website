console.log("Welcome to GQS!");


const track = document.querySelector('.carousel-track');
const items = Array.from(track.children);
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');

let index = 0;

function updateCarousel() {
  const itemWidth = items[0].getBoundingClientRect().width + 30; 
  track.style.transform = `translateX(${-index * itemWidth}px)`;
}

nextBtn.addEventListener('click', () => {
  if (index < items.length - 1) index++;
  updateCarousel();
});

prevBtn.addEventListener('click', () => {
  if (index > 0) index--;
  updateCarousel();
});
