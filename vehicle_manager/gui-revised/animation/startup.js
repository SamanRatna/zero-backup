var animation = bodymovin.loadAnimation({
    container: document.getElementById('startup-page'),
    renderer: 'svg',
    loop: false,
    autoplay: true,
    path: 'animation/startup-1.json'
  });

animation.addEventListener('complete',function(){
    document.getElementById('startup-page').style.display = 'none';
});