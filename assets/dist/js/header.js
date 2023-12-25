// shorten URL: https://tinyurl.com/app
// latex cheat sheet using $..$ or $$...$$: https://alozano.clas.uconn.edu/wp-content/uploads/sites/490/2020/08/latexcheatsheet.pdf
// Katex plugin symbols: https://katex.org/docs/supported.html
// html unicode: https://www.w3schools.com/charsets/ref_emoji_hands.asp

// common data
authorData.set('email', 'Daniel.Zhang@falmouth.ac.uk');
authorData.set('uni', 'Falmouth University');
authorData.set('office', 'Games Academy, Falmouth University');
authorData.set('officehour', 'Monday 13.00-14.00');
authorData.set('classroom', 'Room 1002');
authorData.set('classtime', 'Tuesday & Thursday');
authorData.set('deadline', 'Monday');
authorData.set('name', 'Dr Daniel Zhang');
authorData.set('nickname', 'Daniel');
// add the dynamic item
authorData.set('year', new Date().getFullYear() + " - " + (new Date().getFullYear() + 1));
authorData.set('emaillink', 'mailto:' + authorData.get('email'));
// find course code
let course_code = (authorData.has('coursecode') && authorData.get('coursecode') != '') ? authorData.get('coursecode') + ' - ' : '';

// add title
if (authorData.has('week') && authorData.get('week') != '') {
    let topic = (authorData.has('topic') && authorData.get('topic') != '') ? ' ' + authorData.get('topic') : '';
    authorData.set('title', course_code + authorData.get('course') + ' (' + authorData.get('week') + ') ' + topic);
} else {
    authorData.set('title', course_code + authorData.get('course'));
}
// module name = course name
authorData.set('modulename', authorData.get('course'));
// fullname = name + titles
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
    url = url.substring(0, pos + ".html".length);
    window.location.href = url + "?print-pdf";
}

// for information icon: https://fontawesome.com/v5/search?q=warn&o=r&m=free
authorData.set('info', '<sup><i class="fas fa-exclamation-circle  mediumtext lightred"></i></sup>');
authorData.set('warning', '<sup><i class="fas fa-exclamation-triangle mediumtext orange"></i></sup>');
authorData.set('question', '<sup><i class="fas fa-question-circle mediumtext purple"></i></sup>');
// toggle visibility of a given element by its unique id
function toggleShow(ids) {
    console.log('switching visibility of ' + ids);
    let elm = document.getElementById(ids);
    if (elm) {
        console.log('found ');
        console.log(elm);
        if (elm.classList.contains('invisible')) {
            elm.classList.remove('invisible');
        } else {
            elm.classList.add('invisible');
        }
    }
}