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
    let second = CurrentTime.getSeconds();

    hour = hour < 10 ? "0" + hour : hour;
    minute = minute < 10 ? "0" + minute : minute;
    second = second < 10 ? "0" + second : minute;

    // let GetCurrentTime = hour + ":" + minute + ":" + second;
    let GetCurrentTime = hour + ":" + minute;

    // if (hour > 11) {
    //     GetCurrentTime += "p.m."
    // } else {
    //     GetCurrentTime += "a.m."
    // }

    // update the time
    let div = document.getElementsByClassName("pdf_link")[0];
    div.innerHTML = '<a class="link_no_change" href="#" onclick="GeneratePDF();">⇩PDF</a><br><span class="yellow">' + GetCurrentTime + '</span>';
    // update every 10 seconds, doesn't need to be very accurate
    setTimeout(GetTime, 10000);
}