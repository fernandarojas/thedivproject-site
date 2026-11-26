// To send every "Book a visit" button to HubSpot, paste the form or meetings link here:
var HUBSPOT_URL = '';
(function(){
  if (HUBSPOT_URL) document.querySelectorAll('[data-cta]').forEach(function(a){ a.href = HUBSPOT_URL; a.target = '_blank'; a.rel = 'noopener'; });
  var rooms = window.ROOMS || [], img = document.getElementById('tourImg');
  document.querySelectorAll('.room').forEach(function(b){
    b.addEventListener('click', function(){
      var i = +b.dataset.i, r = rooms[i];
      document.querySelectorAll('.room').forEach(function(x){ x.classList.remove('on'); x.setAttribute('aria-pressed','false'); });
      b.classList.add('on'); b.setAttribute('aria-pressed','true');
      img.style.opacity = 0;
      setTimeout(function(){ img.src = r.img; img.alt = r.name; img.style.opacity = 1; }, 150);
      document.getElementById('tourCode').textContent = String(i+1).padStart(2,'0') + ' / ' + String(rooms.length).padStart(2,'0');
      document.getElementById('tourName').textContent = r.name;
      document.getElementById('tourDesc').textContent = r.desc;
    });
  });
  rooms.forEach(function(r){ var p = new Image(); p.src = r.img; });
  var sticky = document.querySelector('.sticky'), hero = document.querySelector('.hero'), visit = document.getElementById('visit');
  if ('IntersectionObserver' in window && sticky) {
    var seen = {};
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ seen[e.target.id || 'hero'] = e.isIntersecting; });
      sticky.classList.toggle('hide', !!(seen.hero || seen.visit));
    });
    io.observe(hero); io.observe(visit);
  }
})();
