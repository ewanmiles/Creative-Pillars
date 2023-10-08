const LOGGER = document.getElementById('logWindow');
const VISUALISER = document.getElementById('contentVisualiser');
const SELECTOR = document.getElementById('platforms');
var INDEX = 0;

eel.expose(log);
/**
 * Basic logging function for the log window. Adds <p> tag to the window with given text.
 * @param {str} text - String to log to the window
 */
function log(text) {
    LOGGER.innerHTML += `<p>${text}</p>`;
}

eel.expose(loadInContent);
/**
 * YADA YADA YADA
 */
function loadInContent(caption, url, label) {
    VISUALISER.src = url + "embed/";
    document.getElementById('currentLabel').innerText = label;
    document.getElementById('caption').innerText = caption;
}

/**
 * YADA YADA YADA
 */
function js_setFocus(val) {
    eel.loadFirstPost(val)
    INDEX = 0;
}

/**
 * YADA YADA YADA
 */
function loadIndex() {
    platform = SELECTOR.value;
    eel.loadPostIndex(platform, INDEX);
}

function loadNextPost() {
    INDEX += 1;
    loadIndex();
}

function loadPrevPost() {
    INDEX -= 1;
    loadIndex();
}

/**
 * YADA YADA YADA
 * @param {str} val 
 */
function js_labelPost() {
    platform = SELECTOR.value;
    let label = document.getElementById('label').value;
    eel.py_labelPost(platform, INDEX, label);
    document.getElementById('currentLabel').innerText = label;
}

/**
 * YADA YADA YADA
 */
function exportLabels() {
    eel.exportSheet(SELECTOR.value);
    eel.calculateRates(SELECTOR.value);
}