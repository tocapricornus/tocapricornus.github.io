(function () {
let gtag = document.querySelector('meta[name="analytics_gtag"]').content;
window.dataLayer = window.dataLayer || [];
})();

function gtag(){
    dataLayer.push(arguments);
}
gtag('js', new Date());
gtag('config', gtag);
