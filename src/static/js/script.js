/* ===================================
--------------------------------------
  UrbanDictinary - Slang Website Script
  Version: 1.0
--------------------------------------
======================================*/


/* Contents of Javascript
 * 1
 *
 * 
 */

// Dropdown Function
function dropFunc() {
    document.getElementById("menu").classList.toggle("show");
    document.getElementById("dd").classList.toggle("caret-rotate");
}

// window.onclick = function(event) {
//     if (!event.target.matches('.dropBtn')){
//         var dropdowns = document.getElementsByClassName('ddcontent');
//         var i;
//         for (i = 0; i < dropdowns.length; i++) {
//             var openDropdown = dropdowns[i];
//             if (openDropdown.classList.contains('show')){
//                 openDropdown.classListremove('show');
//             }
//         }
//     }
// }

// User Dropdown
function userMenu() {
    document.getElementById("u-menu").classList.toggle("show");
    document.getElementById("caret").classList.toggle("caret-rotate");
}

// const dropdowns = document.getElementById("drops");

// dropdowns.forEach(dropdown => {
//     const select = dropdown.getElementById('user-menu');
//     const caret = dropdown.querySelector('.caret');
//     const menu = dropdown.querySelector('.menu');
//     const items = dropdown.querySelector('.menu li');

//     select.addEventListener('click', () => {
//         caret.classList.toggle('caret-rotate');
//         menu.classList.toggle('show');
//     });
    
//     items.forEach(item => {
//         item.addEventListener('click', () => {
//             caret.classList.remove('caret-rotate');
//             menu.classList.remove('show');
//         });
//     });
// });

// Toggle Popup
function togglePopUp() {
    document.getElementById("List-Tags").classList.toggle("active");
}

// Up and Down votes
var positive = document.getElementById('positive');
var negative = document.getElementById('negative');

function toggleP() {
    if (positive.style.color == "#402E32") {
        positive.style.color = "#205EFF"
    }
    else {
        positive.style.color = "#402E32"   
    }
}

function toggleN() {
    if (negative.style.color == "#402E32") {
        negative.style.color = "#FF002E"
    }
    else {
        negative.style.color = "#402E32"   
    }
}

// Play sounds
function playSound(soundSrc) {
    let audioPlayer = new Audio(soundSrc);
    audioPlayer.play();
    console.log('played ' + soundSrc);
}

// Rating
document.addEventListener("DOMContentLoaded", function() {
    const ratingDivs = document.querySelectorAll('.rating');

    ratingDivs.forEach(div => {
        const ratingValue = parseInt(div.getAttribute('data-rating'));
        addStars(div, ratingValue);
    });

    function addStars(div, rating) {
        n = Math.floor(rating / 20)

        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('span');
            star.className = `star${i <= n ? ' checked' : ''}`;
            star.addEventListener('click', () => handleStarClick(i, div));
            div.appendChild(star);
        }
    }

    // Clickable stars
    // function handleStarClick(starIndex, ratingDiv) {
    //     const stars = ratingDiv.querySelectorAll('.star');
    //     stars.forEach((star, index) => {
    //         star.classList.toggle('checked', index < starIndex);
    //     });

    //     // Update the rating value 
    //     ratingDiv.setAttribute('data-rating', starIndex);
    // }
});

// let stars = document.getElementsByClassName("star");

// function score(n) {
//     if (n == 0) {
//         cls = "zero"
//         for (let h = 0; h < 5; h++) {
//             stars[h].className = "star " + cls;
//         }
//         return;
//     }

//     n = Math.floor(n / 20)
//     for(let i = 0; i < n; i++){
//         if (n == 1) cls = "one";
//         else if (n == 2) cls = "two";
//         else if (n == 3) cls = "three";
//         else if (n == 4) cls = "four";
//         else if (n == 5) cls = "five";
//         stars[i].className = "star " + cls;
//     }
// }

// Change Language
function changeLanguage(languageCode) {
    const form = document.getElementById('languageForm');
    form.elements.language.value = languageCode;
    form.submit();
}