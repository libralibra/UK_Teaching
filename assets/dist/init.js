// Daniel adapted reveal settings

// more settings: https://autonomousvision.github.io/slides/occupancy-flow/lib/reveal/#installation
// Also available as an ES module, see:
// https://revealjs.com/initialization/
Reveal.initialize({
    // Learn about plugins: https://revealjs.com/plugins/
    // and more: https://quarto.org/docs/extensions/listing-revealjs.html
    // https://github.com/hakimel/reveal.js/wiki/Plugins,-Tools-and-Hardware
    // https://github.com/rajgoel/reveal.js-plugins/tree/master

    width: 1200,
    height: 650,

    // 1. has to wait for a fix that Appearance block all fragments for print-pdf version - fixed
    // 2. wait for block in speaker mode fix
    plugins: [RevealZoom, RevealNotes, RevealSearch, RevealMarkdown, RevealHighlight,
        RevealMenu, RevealChalkboard, RevealCustomControls, Verticator,
        RevealMath.KaTeX, RevealPointer, RevealMermaid, Appearance],

    // old style plugins
    dependencies: [
        // ace live code editor 
        { src: '../../../assets/plugin/ace/ace.js' }
    ],

    ace: {
        // Event is triggered when a new editor is created.
        oninit: function (editor) {

        },
        // Event is triggered when the text of an editor has changed
        onchange: function (event, editor) {

        },
        // Automatically focus an editor when it is displayed
        autoFocus: false,

        // defines a css class name for the ace editors
        className: "ace"
    },

    // show controls
    controls: true,
    // show progress bar 
    progress: true,
    // center align slides vertically
    center: true,
    // push each slide in browser history
    history: false,
    // Use 1 based indexing for # links to match slide number (default is zero
    // based)
    hashOneBasedIndex: true,
    // Add the current slide number to the URL hash so that reloading the
    // page/copying the URL will return you to the same slide
    hash: true,
    // Slide number formatting can be configured using these variables:
    //  "h.v": 	horizontal . vertical slide number (default)
    //  "h/v": 	horizontal / vertical slide number
    //    "c": 	flattened slide number
    //  "c/t": 	flattened slide number / total slides
    slideNumber: 'c/t',
    // Control which views the slide number displays on using the "showSlideNumber" value:
    //     "all": show on all views (default)
    // "speaker": only show slide numbers on speaker notes view
    //   "print": only show slide numbers when printing to PDF
    showSlideNumber: 'all',
    // Flags if speaker notes should be visible to all viewers
    showNotes: false,
    // auto play media
    autoPlayMedia: null,
    // preview links, didn't work properly sometimes
    previewLinks: false,

    // make sure slide won't expand more than 1 page in printed pdf
    pdfMaxPagesPerSlide: 1,
    // make sure printed pdf has all fragment in one slide
    pdfSeparateFragments: false,
    // Offset used to reduce the height of content within exported PDF pages.
    // This exists to account for environment differences based on how you
    // print to PDF. CLI printing options, like phantomjs and wkpdf, can end
    // on precisely the total height of the document whereas in-browser
    // printing has to end one pixel before.
    pdfPageHeightOffset: -1,

    // right-arrow works like down arrow or space bar, not grid
    navigationMode: 'linear',
    // mouse wheel navigate
    mouseWheel: false,
    // Focuses body when page changes visibility to ensure keyboard shortcuts work
    focusBodyOnPageVisibilityChange: true,

    // Transition style
    transition: 'concave', // none/fade/slide/convex/concave/zoom
    // Transition speed
    transitionSpeed: 'default', // default/fast/slow
    // Transition style for full page slide backgrounds
    backgroundTransition: 'zoom', // none/fade/slide/convex/concave/zoom

    // disable any preloading
    preloadIframes: false,
    // Number of slides away from the current that are visible
    // this affect the lazy loading behaviours with so many images, videos, and iframes
    // in this case, use <source data-src="video.mp4" type="video/mp4" /> or
    // <source data-src="video.webm" type="video/webm" />
    viewDistance: 3,
    // Number of slides away from the current that are visible on mobile
    // devices. It is advisable to set this to a lower number than
    // viewDistance in order to save resources.
    mobileViewDistance: 2,

    // The display mode that will be used to show slides
    display: 'block',

    // mermaid initialize config
    mermaid: {
        flowchart: {
            // curve will turn off flexible line
            // curve: 'linear',
        },
    },

    // appearance global control
    appearance: {
        // Change this (true/false) if you want to see the shown elements if you go back.
        hideagain: true,
        // Base time in ms between appearances.
        delay: 10,
        // slidetransitionend(default , after the transition)
        // slidechanged(with the transition)
        // auto(with transition, on autoanimate slides)
        appearevent: 'auto',
        // Use this when you do not want to add classes to each item that you want to appear, and just let Appearance add animation classes to (all of) the provided elements in the presentation.
        autoappear: true,
        // These are the elements that autoappear will target. Each element has a selector and an animation class. If autoappear is off, the elements will still get animation if the section contains a data-autoappear attribute.
        // check https://animate.style/ for more styles
        autoelements: {
            "ul li": { "animation": "animate__flipInX", "speed": "faster", "delay": "50" },
            'ol li': {
                "animation": 'animate__jackInTheBox', 'speed': "faster", 'delay': '50'
            },
            // 'img': 'animate__fadeIn',
        },
    },

    // menu options
    menu: {
        // position: left, right
        side: 'left',
        // title with numbers
        numbers: true,
        // click the slide number (original reveal number) open menu
        openSlideNumber: false,
        // add markers to indicate the current slide
        markers: true,
        // transition tab: false or list
        transitions: ['None', 'Fade', 'Slide', 'Concave', 'Convex', 'Zoom'],
        // If slides do not have a matching title, attempt to use the
        // start of the text content as the title instead
        useTextContentForMissingTitles: false,
        // Specifies the path to the default theme files. If your
        // presentation uses a different path to the standard reveal
        // layout then you need to provide this option, but only
        // when 'themes' is set to 'true'. If you provide your own
        // list of themes or 'themes' is set to 'false' the
        // 'themesPath' option is ignored.
        themes: true,
        // with last slash
        themesPath: '../../../assets/dist/theme/',
        // Specify custom panels to be included in the menu, by
        // providing an array of objects with 'title', 'icon'
        // properties, and either a 'src' or 'content' property.
        // custom: false,
        custom: [
            // { title: 'About', icon: '<i class="fa fa-info"></i>', src: 'about.html' },
            {
                title: 'About', icon: '<i class="fa fa-info"></i>',
                content: '<span class="slide-menu-item"><h1>Copyright Disclaimers:</h1><p>All materials used and presented in this slide deck, including images, videos, and photographs, have been collected from the internet for educational purpose only. The copyrights of these materials belong to the original authors who produced them. The author of this presentation does not, and has no intention to, claim any copyrights without explicit statement.</p><br>If you wish to use any of these materials for any other reason, please contact the original authors to obtain proper permissions. If you believe that any content in this presentation violates your copyright, kindly contact me, and I will promptly remove them from the slides.</p></span>' +

                    '<span class="slide-menu-item"><h1>Author:</h1><ul class="slide-menu-items"><li class= "slide-menu-item"><a href="#">Dr Daniel Zhang</li><li class= "slide-menu-item"><a href="#">Date: ' + new Date().getFullYear() + ' - ' + (new Date().getFullYear() + 1) + '</li></span>' +

                    '<span class="slide-menu-item"><h1>Notes:</h1><ul class="slide-menu-items">' +
                    '<li class= "slide-menu-item">? key: to show the help panel</li>' +
                    '<li class= "slide-menu-item">ALT+Click: to zoom in</li>' +
                    '<li class= "slide-menu-item">Q key: turn mouse to pointer</li>' +
                    '</ul></span>'
            },
        ]

    },

    // chalkboard options
    chalkboard: {
        // marker width
        boardmarkerWidth: 5,
        chalkWidth: 7,
        chalkEffect: 1.0,
        storage: null,
        src: null,
        readOnly: undefined,
        transition: 800,
        theme: "chalkboard",
        background: ['rgba(127,127,127,.1)', path + 'img/blackboard.png'],
        grid: { color: 'rgb(50,50,10,0.5)', distance: 80, width: 2 },
        eraser: { src: path + 'img/sponge.png', radius: 20 },
        boardmarkers: [
            { color: 'rgba(220,20,60,1)', cursor: 'url(' + path + 'img/boardmarker-red.png), auto' },
            { color: 'rgba(30,144,255, 1)', cursor: 'url(' + path + 'img/boardmarker-blue.png), auto' },
            { color: 'rgba(50,205,50,1)', cursor: 'url(' + path + 'img/boardmarker-green.png), auto' },
            { color: 'rgba(255,140,0,1)', cursor: 'url(' + path + 'img/boardmarker-orange.png), auto' },
            { color: 'rgba(150,0,20150,1)', cursor: 'url(' + path + 'img/boardmarker-purple.png), auto' },
            { color: 'rgba(255,220,0,1)', cursor: 'url(' + path + 'img/boardmarker-yellow.png), auto' },
            { color: 'rgba(100,100,100,1)', cursor: 'url(' + path + 'img/boardmarker-black.png), auto' },
        ],
        chalks: [
            { color: 'rgba(237, 20, 28, 0.5)', cursor: 'url(' + path + 'img/chalk-red.png), auto' },
            { color: 'rgba(96, 154, 244, 0.5)', cursor: 'url(' + path + 'img/chalk-blue.png), auto' },
            { color: 'rgba(20, 237, 28, 0.5)', cursor: 'url(' + path + 'img/chalk-green.png), auto' },
            { color: 'rgba(220, 133, 41, 0.5)', cursor: 'url(' + path + 'img/chalk-orange.png), auto' },
            { color: 'rgba(220,0,220,0.5)', cursor: 'url(' + path + 'img/chalk-purple.png), auto' },
            { color: 'rgba(255,220,0,0.5)', cursor: 'url(' + path + 'img/chalk-yellow.png), auto' },
            { color: 'rgba(255,255,255,0.5)', cursor: 'url(' + path + 'img/chalk-white.png), auto' },
        ]
    },
    // get more fa icons: https://fontawesome.com/v4/icons/
    // or search in plugin/menu/font-awesome/css/all.css for icon names
    customcontrols: {
        controls: [
            {
                id: 'toggle-overview',
                title: 'Toggle overview (O)',
                // use "fa fa-th" for 3x3 grid
                icon: '<i class="fa fa-th-large"></i>',
                action: 'Reveal.toggleOverview();'
            },
            // {
            //     id: 'toggle-speakernote',
            //     title: 'Toggle speaker mode (S)',
            //     icon: '<i class="fa fa-list-alt"></i>',
            //     action: "Reveal.triggerKey(83);"
            // },
            {
                id: 'toggle-chalkboard',
                icon: '<i class="fa fa-pen-square"></i>',
                title: 'Toggle chalkboard (B)',
                action: 'RevealChalkboard.toggleChalkboard();'
            },
            {
                id: 'toggle-canvas',
                icon: '<i class="fa fa-pen"></i>',
                title: 'Toggle notes canvas (C)',
                action: 'RevealChalkboard.toggleNotesCanvas();'
            },
            {
                id: 'toggle-pause',
                icon: '<i class="fa fa-eye-slash"></i>',
                title: 'Black out the slides (.)',
                action: 'Reveal.togglePause();'
            },
            {
                id: 'toggle-fullscreen',
                // or 'fa fa-expand' for another icon
                icon: '<i class="fa fa-expand"></i>',
                title: 'Toggle fullscreen (F)',
                action: 'document.documentElement.requestFullscreen();'

            },
            {
                id: 'toggle-help',
                icon: '<i class="fa fa-question-circle"></i>',
                title: 'Show help (?)',
                action: 'Reveal.toggleHelp();'

            }
        ]
    },
    // vertical deck indicator
    verticator: {
        color: 'cyan',
        inversecolor: 'blue',
        skipuncounted: true,
        tooltip: 'auto',
        scale: 1.2,
    },
    // pointer
    pointer: {
        key: "q", // key to enable pointer, default "q", not case-sensitive
        color: "#ffca3a", // color of a cursor, default "red" any valid CSS color; red, green, blue, yellow can be set as "#fa1e0e", "#8ac926", "#1982c4", "#ffca3a" 
        opacity: 0.9, // opacity of cursor, default 0.8
        pointerSize: 18, // pointer size in px, default 12
        alwaysVisible: false, // should pointer mode be always visible? default "false"
        tailLength: 10, // NOT IMPLEMENTED YET!!! how long the "tail" should be? default 10
    },
});