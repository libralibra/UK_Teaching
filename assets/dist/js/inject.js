//  =============== INJECT NAME, EMAIL, OFFICE ==============
// set up all data in header, but update the document here

// update html, the emaillink class need to be treated specially, so does the document title
// javascript Map.forEach() loops (value,key) pair rather than (key,value) pair
authorData.forEach((v, k) => {
    // set up key word, is it a class or document title?
    var keyw = k;
    if (k != 'title') keyw = '.' + k;
    // search the entity and replace the content
    document.querySelectorAll(keyw).forEach(element => {
        if (k == 'title') {
            element.textContent = v;
        }
        else if (k == 'emaillink') {
            element.href = v;
            element.innerHTML = '<span>' + authorData.get('email') + '</span>';
        }
        else {
            element.innerHTML = v;
        }
    });
});

// get use the data saved in meta blocks in header
// but not used at the moment
let getMetaContent = (n) => document.querySelector("meta[name='" + n + "']").getAttribute("content");

console.log(getMetaContent('author'));
// console.log(getMetaContent('og:author'));

// show the current time at the top-right corner
GetTime();

function GetTime() {
    let CurrentTime = new Date()
    let hour = CurrentTime.getHours()
    let minute = CurrentTime.getMinutes();
    // let second = CurrentTime.getSeconds();

    hour = hour < 10 ? "0" + hour : hour;
    minute = minute < 10 ? "0" + minute : minute;
    // second = second < 10 ? "0" + second : minute;

    // let GetCurrentTime = hour + ":" + minute + ":" + second;
    let current_time_str = hour + ":" + minute;

    // if (hour > 11) {
    //     GetCurrentTime += "p.m."
    // } else {
    //     GetCurrentTime += "a.m."
    // }

    let span = document.getElementById("time_placeholder");
    span.innerHTML = current_time_str;
    // update every 10 seconds, doesn't need to be very accurate
    setTimeout(GetTime, 10000);
}

// add python console appear and disappear function
const iframe = document.getElementById('mid-iframe');
const textElement = document.getElementById('time_placeholder');

textElement.addEventListener('click', () => {
    iframe.style.display = 'block';
    // Apply ease effect to animate the iframe's position to the center
    // iframe.style.left = '50%';
    // iframe.style.top = '50%';
    iframe.style.left = '50%';
    iframe.style.top = '50%';
    iframe.style.width = '80%';
    iframe.style.height = '41%';
    // width: 80 %;
    // height: 41 %;
    iframe.style.transform = 'translate(-50%, -50%)';
    iframe.style.transition = 'all 0.5s ease';
    iframe.style.opacity = '1';
    iframe.style.zIndex = '1000';
});

iframe.addEventListener('click', () => {
    // Reverse the transform to hide the iframe
    iframe.style.transform = 'translate(-50%, -50%) scaleX(0) scaleY(0)';
    iframe.style.transition = 'all 0.3s ease-out';
    iframe.style.opacity = '0';
    iframe.style.zIndex = '-10';
});