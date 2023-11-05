// LINKS EFFECT: https://jsfiddle.net/hakim/Ht6Ym/

var supports3DTransforms = document.body.style['webkitPerspective'] !== undefined ||
    document.body.style['MozPerspective'] !== undefined;

function linkify(selector) {
    if (supports3DTransforms) {

        var nodes = document.querySelectorAll(selector);

        for (var i = 0, len = nodes.length; i < len; i++) {
            var node = nodes[i];
            if (!node.className || !node.className.match(/roll/g)) {
                // exclude the image links, has img as a children, for firefox not supporting :has()
                if (node.querySelector('img')) continue;
                // parents div is not slide-number
                if (node.parentNode.className.match(/slide-number/gi)) continue;
                node.className += ' roll';
                node.innerHTML = '<span data-title="' + node.text + '">' + node.innerHTML + '</span>';
            }
        };
    }

}
// don't apply to image links, firefox doesn't support :has() for the time being, manually exclude those link in function
// linkify('a:not(.slide-number):not(:has(img))');
linkify('a');