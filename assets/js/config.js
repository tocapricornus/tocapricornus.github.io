/**
 * Config
 * -------------------------------------------------------------------------------------
 * ! IMPORTANT: Make sure you clear the browser local storage In order to see the config changes in the template.
 * ! To clear local storage: (https://www.leadshook.com/help/how-to-clear-local-storage-in-google-chrome-browser/).
 */

'use strict';

// JS global variables
let config = {
  colors: {
    primary: '#696cff',
    secondary: '#8592a3',
    success: '#71dd37',
    info: '#03c3ec',
    warning: '#ffab00',
    danger: '#ff3e1d',
    dark: '#233446',
    black: '#000',
    white: '#fff',
    body: '#f4f5fb',
    headingColor: '#566a7f',
    axisColor: '#a1acb8',
    borderColor: '#eceef1'
  }
};

function loadScript(src, g, async, crossorigin) {
  let script = document.createElement('script');
  script.src = src;
  script.async = async;
  if('' != crossorigin) script.crossorigin = crossorigin;
  if(g == 'body'){
    document.body.append(script);
  }else if(g == 'head'){
    document.head.append(script);
  }
}

window.addEventListener('load', function() {
  var allElements = document.getElementsByTagName('*');
  Array.prototype.forEach.call(allElements, function(el) {
      var includePath = el.dataset.includePath;
      if (includePath) {
          var xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function () {
              if (this.readyState == 4 && this.status == 200) {
                  el.outerHTML = this.responseText;
              }
          };
          xhttp.open('GET', includePath, true);
          xhttp.send();
        }
      });
      let adsense_client = document.querySelector('meta[name="google-adsense-account"]').content;
      
      if (adsense_client !== ''){
        loadScript('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='+adsense_client, 'head', true, 'anonymous' );
        loadScript('/assets/js/google_search.js', 'body', false);
        loadScript('https://www.googletagmanager.com/gtag/js?id=G-LGGMTY7TLB', 'head', true);
        loadScript('/assets/js/gtag.js', 'head', false);

      }

      loadScript('/assets/vendor/js/helpers.js', 'body', false);
      loadScript('/assets/vendor/libs/jquery/jquery.js', 'body', false);
      loadScript('/assets/vendor/js/bootstrap.js', 'body', false);
      loadScript('/assets/vendor/libs/perfect-scrollbar/perfect-scrollbar.js', 'body', false);
      loadScript('/assets/vendor/js/menu.js', 'body', false);
      loadScript('/assets/js/main.js', 'body', false);
});
