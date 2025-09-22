// // Back to top functionality
// document.addEventListener('DOMContentLoaded', function() {
//     const backToTop = document.getElementById('back-to-top');
    
//     if (backToTop) {
//         window.addEventListener('scroll', function() {
//             if (window.pageYOffset > 300) {
//                 backToTop.classList.remove('opacity-0', 'translate-y-10');
//                 backToTop.classList.add('opacity-100', 'translate-y-0');
//             } else {
//                 backToTop.classList.remove('opacity-100', 'translate-y-0');
//                 backToTop.classList.add('opacity-0', 'translate-y-10');
//             }
//         });
        
//         backToTop.addEventListener('click', function() {
//             window.scrollTo({
//                 top: 0,
//                 behavior: 'smooth'
//             });
//         });
//     }
    
//     // HTMX configuration
//     document.body.addEventListener('htmx:configRequest', function(evt) {
//         // Add any custom headers or configuration
//     });
    
//     // Lazy loading for images
//     if ('loading' in HTMLImageElement.prototype) {
//         const images = document.querySelectorAll('img[loading="lazy"]');
//         images.forEach(img => {
//             img.src = img.dataset.src;
//         });
//     }
// });