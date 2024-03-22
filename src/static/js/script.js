function dropFunc() {
    document.getElementById("menu").classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropBtn')){
        var dropdowns = document.getElementsByClassName('ddcontent');
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')){
                openDropdown.classListremove('show');
            }
        }
    }
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

    function handleStarClick(starIndex, ratingDiv) {
        const stars = ratingDiv.querySelectorAll('.star');
        stars.forEach((star, index) => {
            star.classList.toggle('checked', index < starIndex);
        });

        // Update the rating value (you may want to send it to the server)
        ratingDiv.setAttribute('data-rating', starIndex);
    }
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