// Reference to the creative's various properties and elements.
var creative = {};

var dynamicBuilder = {};

dynamicBuilder.data = [];

/**
 * Called on the window load event.
 */
function preInit() {
  if (Enabler.isInitialized()) {
    init();
  } else {
    Enabler.addEventListener(studio.events.StudioEvent.INIT, init);
  }
}

/**
 * Set up references to DOM elements.
 */
function setupDom() {
  creative.dom = {};
  creative.dom.mainContainer = document.querySelector(
    ".dynamicAdvertContainer"
  );
  creative.dom.data = {};
  creative.dom.data.url = dynamicContent.data[0].Data_Url;
  creative.dom.exit = {};
  creative.dom.exit.url = dynamicContent.data[0].Exit_Url.Url;
}

/**
 * The Enabler is now initialized and any extra modules have been loaded.
 */
function init() {
  setupDom();
  buildData();
}

function buildData() {
  var xobj = new XMLHttpRequest();
  var url = creative.dom.data.url;
  xobj.overrideMimeType("application/json");
  xobj.open("GET", url, true);
  xobj.onreadystatechange = function() {
    if (xobj.readyState == 4 && xobj.status == "200") {
      var data = xobj.responseText;
      var parsedData = JSON.parse(data);
      var target = ".dynamicAdvertContainer";

      buildDOM(target, parsedData);
      addListeners();
      // Polite loading
      if (Enabler.isVisible()) {
        show();
      } else {
        Enabler.addEventListener(studio.events.StudioEvent.VISIBLE, show);
      }
    }
  };
  xobj.send(null);
}

/**
 * Add appropriate listeners after the creative's DOM has been set up.
 */
function addListeners() {
  document.getElementById("exit").addEventListener("click", exitClickHandler);
}

/**
 *  Shows the ad.
 */
function show() {
  creative.dom.mainContainer.style.display = "block";
  startAnimation(0);
}

// ---------------------------------------------------------------------------------
// MAIN
// ---------------------------------------------------------------------------------

function exitClickHandler() {
  Enabler.exitOverride("DynamicExit", creative.dom.exit.url);
}

/**
 *  Main onload handler
 */
window.addEventListener("load", preInit);
