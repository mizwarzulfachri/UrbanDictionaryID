/* ===================================
--------------------------------------
  UrbanDictinary - Slang Website Script
  Version: 1.0
--------------------------------------
======================================*/

/*----------------------------------------*/
/* Template default Script
/*----------------------------------------*/


/*----------------------------------------*/
/* Contents of Javascript
/*----------------------------------------*/

/* 1 - Base Html
 * 2 - User Dropdown
 * 3 - User Dropdown
 * 4 - Loader
 * 5 - Up and Down votes
 * 6 - Play sounds
 * 7 - Rating
 * 8 - Change Language
 * 9 - Peak Password
 * 10 - Tab Change
 */

/*----------------------------------------*/
/* 1 Dropdown Function
/*----------------------------------------*/
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

/*----------------------------------------*/
/* 2 User Dropdown
/*----------------------------------------*/
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

/*----------------------------------------*/
/* 3 - Toggle Popup
/*----------------------------------------*/
function togglePopUp() {
    document.getElementById("List-Tags").classList.toggle("active");
}

/*----------------------------------------*/
/* 4 Loader
/*----------------------------------------*/
window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");

    loader.classList.add("loader-hidden");

    loader.addEventListener("transitionend", () => {
        document.body.removeChild("loader");
    })
})

/*----------------------------------------*/
/* 5 Up and Down votes
/*----------------------------------------*/
var positive = document.getElementById('positive');
var negative = document.getElementById('negative');

function toggleP() {
    positive.style.color = "#205EFF"
}

function toggleN() {
    negative.style.color = "#FF002E"
}

/*----------------------------------------*/
/* 6 Play sounds
/*----------------------------------------*/
function playSound(soundSrc) {
    let audioPlayer = new Audio(soundSrc);
    audioPlayer.play();
    console.log('played ' + soundSrc);
}

/*----------------------------------------*/
/* 7 Rating
/*----------------------------------------*/
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

/*----------------------------------------*/
/* 8 Change Language
/*----------------------------------------*/
function changeLanguage(languageCode) {
    const form = document.getElementById('languageForm');
    form.elements.language.value = languageCode;
    form.submit();
}

/*----------------------------------------*/
/* 9 Peak Password
/*----------------------------------------*/
let eyeicon1 = document.getElementById("eye-icon1");
let password1 = document.getElementById("password1");

eyeicon1.onclick = function() {
    if(password1.type == "password") {
        password1.type = "text";
        eyeicon1.className = 'fa fa-eye';
    } else {
        password1.type = "password";
        eyeicon1.className = 'fa fa-eye-slash';
    }
}

let eyeicon2 = document.getElementById("eye-icon2");
let password2 = document.getElementById("password2");

eyeicon2.onclick = function() {
    if(password2.type == "password") {
        password2.type = "text";
        eyeicon2.className = 'fa fa-eye';
    } else {
        password2.type = "password";
        eyeicon2.className = 'fa fa-eye-slash';
    }
}

let eyeicon0 = document.getElementById("eye-icon0");
let password0 = document.getElementById("password0");

eyeicon0.onclick = function() {
    if(password0.type == "password") {
        password0.type = "text";
        eyeicon0.className = 'fa fa-eye';
    } else {
        password0.type = "password";
        eyeicon0.className = 'fa fa-eye-slash';
    }
}

/*----------------------------------------*/
/* 10 Tab Change
/*----------------------------------------*/
const tabs = document.querySelectorAll('.tab-btn');
const all_content = document.querySelectorAll('.tab-content');

tabs.forEach((tab, index)=> {
    tab.addEventListener('click', (e)=>{
        tabs.forEach(tab=>{tab.classList.remove('active')});
        tab.classList.add('active');

        var line = document.querySelector('.line');
        line.style.width = e.target.offsetWidth + "px";
        line.style.left = e.target.offsetLeft + "px";

        all_content.forEach(content=>{content.classList.remove('active')})
        all_content[index].classList.add('active');
    });
});