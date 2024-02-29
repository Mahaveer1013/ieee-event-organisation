// Function to animate counting
// function animateCount(element, targetCount) {
//     let currentCount = 0;
//     const duration = 150; // Adjust the duration as needed
//     const step = targetCount / duration;

//     function updateCount() {
//         currentCount += step;
//         element.textContent = `${Math.ceil(currentCount)}+`;

//         if (currentCount < targetCount) {
//             requestAnimationFrame(updateCount);
//         }
//     }

//     updateCount();
// }

// Intersection Observer to trigger counting animation when element is in view
// const countBox = document.getElementById('countBox');
// const counters = document.querySelectorAll('.count');

// const observer = new IntersectionObserver(entries => {
//     entries.forEach(entry => {
//         if (entry.isIntersecting) {
//             counters.forEach(counter => {
//                 const targetCount = parseInt(counter.textContent);
//                 animateCount(counter, targetCount);
//             });
//             observer.disconnect();
//         }
//     });
// }, { threshold: 0.5 });

// observer.observe(countBox);

const targetDate = new Date("March 4, 2024 00:00:00").getTime();

// Function to update the countdown timer
function updateCountdown() {
  const now = new Date().getTime();
  const timeDifference = targetDate - now;

  const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
  const hours = Math.floor(
    (timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
  );
  const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

  if (timeDifference <= 0) {
    // Countdown reached, you can handle this event as needed
    document.getElementById("countdown").innerHTML =
      '<p class="count" style="font-size: 30px;" >Event has started !</p>';
  } else {
    document.querySelector(".days").innerText = `${days} d`;
    document.querySelector(".hours").innerText = `${hours} hrs`;
    document.querySelector(".mins").innerText = `${minutes} mins`;
    document.querySelector(".secs").innerText = `${seconds} secs`;
  }
}

// Update the countdown every second
setInterval(updateCountdown, 1000);

// Initial call to set the countdown on page load
updateCountdown();
