// =========== change overview scales ====================
// regexp to match only the last `scale(...)` rule (there are two scale rules on the .slides element, don't know why)
const currentScaleRegexp = /scale\([^\)]*\)(?!.*(scale))/;
// prevent infinite loop https://stackoverflow.com/a/48599188
let insideInitialObserverCallback = false;

let observer = new MutationObserver(mutationsList => {
    // only react when in overview mode
    // could also use https://revealjs.com/overview/#events to stop/start observer when needed
    if (!Reveal.isOverview()) return;

    insideInitialObserverCallback = !insideInitialObserverCallback
    if (insideInitialObserverCallback) {
        mutationsList.forEach(mutation => {
            const currentTransform = mutation.target.style.transform;
            // change to the scale that fits your needs
            // mutation.target.style.transform = currentTransform.replace(currentScaleRegexp, 'scale(.05)');
            mutation.target.style.transform = currentTransform.replace(currentScaleRegexp, 'scale(' + overview_scale.toString() + ')');
        })
    }
});
observer.observe(
    Reveal.getSlidesElement(),
    { attributes: true, attributesFilter: ['style'] }
);