// move all js including into a separate file
// Daniel, Oct 2023
document.write(`
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

<!-- the main js file -->
<script src="../../../assets/dist/reveal.js"></script>

<!-- the default plugins -->
<script src="../../../assets/plugin/zoom/zoom.js"></script>
<script src="../../../assets/plugin/notes/notes.js"></script>
<script src="../../../assets/plugin/search/search.js"></script>
<script src="../../../assets/plugin/markdown/markdown.js"></script>
<script src="../../../assets/plugin/highlight/highlight.js"></script>

<!-- math -->
<script src="../../../assets/plugin/math/math.js"></script>

<!-- menu: https://github.com/denehyg/reveal.js-menu -->
<script src="../../../assets/plugin/menu/menu.js"></script>

<!-- chalkboard need customcontrols, has to be included together -->
<script src="../../../assets/plugin/chalkboard/plugin.js"></script>
<script src="../../../assets/plugin/customcontrols/plugin.js"></script>

<!-- appearance for element (text and image) animation like ppt -->
<script src="../../../assets/plugin/appearance/appearance.js"></script>

<!-- vertical deck indicator: verticator -->
<script src="../../../assets/plugin/verticator/verticator.js"></script>

<!-- pointer, press Q to turn it on -->
<script src="../../../assets/plugin/pointer/pointer.js"></script>

<!-- mermaid flowchart -->
<script src="../../../assets/plugin/mermaid/mermaid.js"></script>

<!-- copy code -->
<script src="../../../assets/plugin/copycode/copycode.js"></script>

<!-- make long slides overflow -->
<script id="overflow" src="../../../assets/dist/js/overflow.js"></script>

<!-- change overview scale -->
<script id="overview_scale" src="../../../assets/dist/js/overview_scale.js"></script>

<!-- ===============INJECT NAME, EMAIL, OFFICE ============== -->
<script id="inject_data" src="../../../assets/dist/js/inject.js"></script>

<!-- LINKS EFFECT: https://jsfiddle.net/hakim/Ht6Ym/  -->
<script id="linkify" src="../../../assets/dist/js/linkify.js"></script>

<!-- sync image alt and title strings -->
<script id="check_image" src="../../../assets/dist/js/check_images.js"></script>

<!-- it did copy the logo to each slide in the print preview,
    but not in the ctrl+p generated pdf file, so wont' be printed.
    wait for bug fix -->
<script id="copy_logo" src="../../../assets/dist/js/copy_logo.js"></script>

<!-- reveal initialisation -->
<script id="reveal_init" src="../../../assets/dist/js/init.js"></script>
`);