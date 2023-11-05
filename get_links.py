''' Use this script to generate all links to existing files for easily deploying
    slide decks to github as the URLs would be different
    Use relative link in the index.html page to make it generic between repositories

    The structure would be:

    <div class="reveal">
        <div class="slides">
            <section id="EACH UNIVERSITY">
                <section id="EACH MODULE">
                    <!-- list each html file here -->
                </section>
            </section>
        </div>
    </div>

    Daniel.Zhang
    Oct 2023
'''

# importing modules
import os
from glob import glob

HEADERS = r'''<!doctype html>
<html lang="en">

    <head>
        <title></title>

        <!-- charset setting -->
        <meta charset="utf-8">

        <!-- meta data -->
        <meta name="author" content="Dr Daniel Zhang">
        <meta name="generator" content="VS Code">

        <!-- disable search engine robots -->
        <meta name="robots" content="none">

        <!-- viewport settings -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

        <link rel="stylesheet" href="./assets/dist/css/master.css">

        <!-- all links open in new tab -->
        <!-- <base target="_blank"> -->

        <!-- define data here, but update the document later to avoid using
                window.onload = function() {}; syntax -->
        <script>
            const authorData = new Map([
                ['course', "Daniel's Teaching Materials"],
                ['coursecode', ''],
                ['week', 'For UK Universities'],
                ['topic', 'Categorised by Modules'],
            ]);
        </script>
        <script id="header_pdf_func" src="./assets/dist/js/header.js"></script>
    </head>

    <body>
        <!-- pdf printing by showing a corner strip+
                    put pdf button before anything else, as the z-index makes sure later elements has a 
                    higher z-index than those before. In overview mode, the slides should be in the front.
                -->
        <div class="pdf_div">
            <div class="pdf_link" title="Save Slides as PDF" onclick="GeneratePDF();"><a class="link_no_change" href='#'>⇩PDF</a></div>
        </div>

        <!-- main content of the slides -->
        <div class="reveal">
            <!-- Any section element inside of this container is displayed as a slide -->
            <div class="slides">
'''

FOOTER = r'''</div>
        </div>

        <!-- header footer div -->
        <div id="header">
            <!-- <div id="header-left">HEADER-LEFT</div> -->
            <!-- <div id="header-right">HEADER-RIGHT</div> -->
            <div class="footer-left"><a href="https://github.com/libralibra/UK_Teaching" target="_blank"><img class="img-width-100 img-round-corner-10 img-zoom-15 fix-bottom-left" src="https://www.analyticsvidhya.com/wp-content/uploads/2015/07/github_logo-1024x219.png" title="visit GitHub Repository"></a></div>
            <!-- <div id="footer-right">FOOTER-RIGHT</div> -->
        </div>

        <!-- keys: 
            SPACE,arrow :   navigation
            .           :   blackout
            ESC, O      :   overview
            ALT+click   :   zoom in
            C           :   note canvas
            B           :   chalkboard
            S           :   speaker mode (appearance didn't work well with speaker mode)
            C+S+F       :   search in slides

        -->

        <script src="./assets/dist/reveal.js"></script>
        <script src="./assets/plugin/zoom/zoom.js"></script>
        <script src="./assets/plugin/notes/notes.js"></script>
        <script src="./assets/plugin/search/search.js"></script>
        <script src="./assets/plugin/markdown/markdown.js"></script>
        <script src="./assets/plugin/highlight/highlight.js"></script>
        <!-- math -->
        <script src="./assets/plugin/math/math.js"></script>
        <!-- menu: https://github.com/denehyg/reveal.js-menu -->
        <script src="./assets/plugin/menu/menu.js"></script>
        <!-- chalkboard need customcontrols -->
        <script src="./assets/plugin/chalkboard/plugin.js"></script>
        <script src="./assets/plugin/customcontrols/plugin.js"></script>
        <!-- appearance for text and image animation like ppt -->
        <!-- <script src="./assets/plugin/appearance/appearance.js"></script> -->
        <!-- vertical deck indicator: verticator -->
        <script src="./assets/plugin/verticator/verticator.js"></script>
        <!-- pointer -->
        <script src="./assets/plugin/pointer/pointer.js"></script>
        <!-- mermaid flowchart -->
        <script src="./assets/plugin/mermaid/mermaid.js"></script>

        <!-- reveal initialisation -->
        <script id="reveal_init">
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

                // plugins: [RevealZoom, RevealNotes, RevealSearch, RevealMarkdown, RevealHighlight, RevealMenu, RevealChalkboard, RevealCustomControls, Appearance, Verticator],

                // old style plugins
                dependencies: [
                    // ace live code editor 
                    { src: './assets/plugin/ace/ace.js' }
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

                // 1. has to wait for a fix that Appearance block all fragments for print-pdf version - fixed
                // 2. wait for block in speaker mode fix
                plugins: [RevealZoom, RevealNotes, RevealSearch, RevealMarkdown, RevealHighlight,
                    RevealMenu, RevealChalkboard, RevealCustomControls, 
                    Verticator, RevealMath.KaTeX, RevealPointer, RevealMermaid],

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
                transition: 'convex', // none/fade/slide/convex/concave/zoom
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
                        curve: 'linear',
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
                    themesPath: './assets/dist/theme/',
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
        </script>

        <!-- make long slides overflow -->
        <script id="overflow" src="./assets/dist/js/overflow.js"></script>

        <!-- change overview scale -->
        <script id="overview_scale" src="./assets/dist/js/overview_scale.js"></script>

        <!-- ===============INJECT NAME, EMAIL, OFFICE ============== -->
        <script id="inject_data" src="./assets/dist/js/inject.js"></script>

        <!-- LINKS EFFECT: https://jsfiddle.net/hakim/Ht6Ym/  -->
        <script id="linkify" src="./assets/dist/js/linkify.js"></script>

        <!-- sync image alt and title strings -->
        <script id="check_image" src="./assets/dist/js/check_images.js"></script>

        <!-- it did copy the logo to each slide in the print preview,
            but not in the ctrl+p generated pdf file, so wont' be printed.
            wait for bug fix -->
        <script id="copy_logo" src="./assets/dist/js/copy_logo.js"></script>

    </body>
</html>'''

# #################################################################
def get_all_files(d_path):
    ''' get all files with relative links to a dict: {uni: {module:html}} '''
    # get all html file paths 
    htmls = [x[x.index(d_path)+len(d_path)+1:] for x in glob(d_path+r'/**/*.html',recursive=True)]
    # sort out after split: uni -> module -> htmls
    html_dict = {}
    for x in htmls:
        parts = x.split(os.sep)
        u,m,f = parts[0],parts[1],os.sep.join(parts[2:])
        if u in html_dict:
            if m in html_dict[u]:
                html_dict[u][m].append(f)
            else:
                html_dict[u][m] = [f]
        else:
            html_dict[u] = {m:[f]}
    return html_dict

# #################################################################
SECTION_START = r'''<section id="chapter_UNIVERSITY">
                    <section id="UNIVERSITY">
                        <h1 class="r-frame-text">UNIVERSITY</h1>
                    </section>'''
SECTION_END = r'</section>'
def get_uni_section(base_path, u_name, u_modules):
    ''' create a section (a new vertical slide deck) for each university
        base_path: where start the search
        u_name: university name
        u_modules: a dict of m_name -> list of html files
    '''
    return SECTION_START.replace('UNIVERSITY',u_name) + '\n'.join([get_module_slide(base_path+'/'+u_name,k,v) for k,v in u_modules.items()]) + SECTION_END

# #################################################################  
MODULE_LEFT = r'''
<section id="MODULE">
    <h1>MODULE</h1><ol>
    <div class="row no-margin-top no-margin-bottom r-stretch">
        <div class="col-50 no-margin-top">
'''
MODULE_RIGHT = r'''</div>
<div class="col-50 no-margin-top">'''
MODULE_END = r'''</div></div></ol>
</section>'''
def get_module_slide(u_name, m_name, m_htmls):
    ''' get a module page using it's name (slide id), and all it's children html files as the page content 
        u_name: university name (added to the path)
        m_name: module name (the header and added to the path)
        m_htmls: a list of all html files
    '''
    left = [f'<li><a href="{u_name}/{m_name}/{h}">{h}</a></li>' for h in m_htmls[:round(len(m_htmls)/2+0.5)]]
    right = [f'<li><a href="{u_name}/{m_name}/{h}">{h}</a></li>' for h in m_htmls[round(len(m_htmls)/2+0.5):]]
    return MODULE_LEFT.replace('MODULE',m_name) + '\n'.join(left) + MODULE_RIGHT + '\n'.join(right) + MODULE_END

# #################################################################
# global definitions
BASE_UNI_URL = r'https://pages.github.falmouth.ac.uk/Daniel-Zhang/UK_Teaching/'
BASE_PRI_URL = r'https://libralibra.github.io/UK_Teaching/'
SOURCE_PATH = r'Uni'
OUTPUT_PATH = r'all_links.html'
def get_html(base_path, h_dict):
    ''' write out the html file: '''
    with open(OUTPUT_PATH,'w',encoding="utf-8") as fout:
        fout.write(HEADERS + '\n'.join([get_uni_section(SOURCE_PATH,u,m) for u,m in h_dict.items()]) + FOOTER)
    print(f'{OUTPUT_PATH} has been updated!')


# #################################################################
if __name__ == '__main__':
    htmls = get_all_files(SOURCE_PATH)
    print(len(htmls),'->',htmls)
    get_html(SOURCE_PATH,htmls)

