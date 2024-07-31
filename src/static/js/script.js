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
 * 9 - Database
 * 10 - Peak Password
 * 11 - Tab Change
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
    });
});

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
/* 9 Tab Change
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

        all_content.forEach(content=>{content.classList.remove('active')});
        all_content[index].classList.add('active');
    });
});

/*----------------------------------------*/
/* 10 Database
/*----------------------------------------*/
const page = document.querySelectorAll('aside div a');

page.forEach((p) => {
    p.addEventListener('click', () => {
        document.querySelector('.active').classList.remove('active');
        p.classList.add('active');
    });
});

function setActive(el) {
    const currentUrl = el.getAttribute('href');
    const classSelector = currentUrl.replace('#', '.');

    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    const currentContent = document.querySelector(classSelector);
    if (currentContent) {
        currentContent.classList.add('active');
    }
}

let srch_w = document.getElementById('search-word');
let srch_u = document.getElementById('search-user');
let srch_c = document.getElementById('search_tag');

srch_w?.addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const hash = '#Word';
    const searchQuery = form.querySelector('input[name="s"]').value;

    let actionUrl = form.action;
    if (searchQuery) {
        actionUrl += `?s=${encodeURIComponent(searchQuery)}${hash}`;
    } else {
        actionUrl += hash;
    }

    window.location.href = actionUrl;
});

srch_u?.addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const hash = '#User';
    const searchQuery = form.querySelector('input[name="u"]').value;

    let actionUrl = form.action;
    if (searchQuery) {
        actionUrl += `?u=${encodeURIComponent(searchQuery)}${hash}`;
    } else {
        actionUrl += hash;
    }

    window.location.href = actionUrl;
});

srch_c?.addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const hash = '#Tag';
    const searchQuery = form.querySelector('input[name="c"]').value;

    let actionUrl = form.action;
    if (searchQuery) {
        actionUrl += `?c=${encodeURIComponent(searchQuery)}${hash}`;
    } else {
        actionUrl += hash;
    }

    window.location.href = actionUrl;
});

function redirectToWord(url) {
    const changeUrl = `${url}#Word`;

    window.location.href = changeUrl;
}

function redirectToReport(url) {
    const changeUrl = `${url}#Report`;

    window.location.href = changeUrl;
}

/*----------------------------------------*/
/* 11 Check Redirect
/*----------------------------------------*/
function checkHash() {
    const hash = window.location.hash;
    if (hash) {
        const classSelector = hash.replace('#', '.');
        
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        const currentContent = document.querySelector(classSelector);
        if (currentContent) {
            currentContent.classList.add('active');
        }

        document.querySelectorAll('.side_link').forEach(link => {
            if (link.getAttribute('href') === hash) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', checkHash);
window.addEventListener('hashchange', checkHash);

/*----------------------------------------*/
/* 12 Peak Password
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