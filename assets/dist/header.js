// add the dynamic item
authorData.set('year', new Date().getFullYear() + " - " + (new Date().getFullYear() + 1));
authorData.set('emaillink', 'mailto:' + authorData.get('email'));
if (authorData.has('week')) {
    authorData.set('title', authorData.get('course') + '-' + authorData.get('week'));
} else {
    authorData.set('title', authorData.get('course'));
}

authorData.set('modulename', authorData.get('course'));
authorData.set('fullname', authorData.get('name') + ' (PhD, MSc, BEng)');
// CALL THE FUNCTION TO UPDATE DOCUMENT IN THE END

// overview scale
overview_scale = 0.2;

// generate pdf link, click the button, then press CTRL+P
// remember to follow these steps to get rid of the borders:
//  1. select 'save as PDF' for printer
//  2. advanced settings or something similar
//  3. margin -> None if needed
//  4. tick 'background graphics' if needed
function GeneratePDF() {
    let url = window.location.href;
    let pos = url.indexOf(".html");
    url = url.substr(0, pos + ".html".length);
    window.location.href = url + "?print-pdf";
}