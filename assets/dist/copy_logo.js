// another method and the author's reply
// https://github.com/hakimel/reveal.js/issues/806

// this one did work and worth checking
// http://www.ciges.net/revealjs_demo

// it did copy the logo to each slide in the print preview,
// but not in the ctrl + p generated pdf file, so wont' be printed.
// wait for bug fix

// depends on the id in the slide, choose the proper selector
// var header = document.querySelector('#header');
// var logo = document.querySelector('.footer-left');
// Reveal.on('pdf-ready', () => {
//     // change style for pdf print mode
//     logo.classList.add('footer-left-pdf');
//     logo.classList.remove('footer-left');
//     // copy the logo except the title
//     document.querySelectorAll('.pdf-page').forEach(function (page, index) {
//         // jump over the title page as it's already shown
//         // if (index != 0) page.appendChild(logo.cloneNode(true));
//         page.appendChild(logo.cloneNode(true));
//     });
// });