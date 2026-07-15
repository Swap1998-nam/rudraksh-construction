(function(){
  // mobile nav
  var navToggle = document.getElementById('navToggle');
  var navList = document.getElementById('navList');
  if (navToggle && navList) {
    navToggle.addEventListener('click', function(){ navList.classList.toggle('open'); });
    navList.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){ navList.classList.remove('open'); });
    });
  }

  // scroll reveal
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, {threshold:0.15});
    revealEls.forEach(function(el){ io.observe(el); });
  } else {
    revealEls.forEach(function(el){ el.classList.add('in'); });
  }

  // gallery filter
  var filterBtns = document.querySelectorAll('.filter-btn');
  var galItems = document.querySelectorAll('.gal-item');
  filterBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      filterBtns.forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      var f = btn.getAttribute('data-filter');
      galItems.forEach(function(item){
        if (f === 'all' || item.getAttribute('data-cat') === f) {
          item.classList.remove('hide');
        } else {
          item.classList.add('hide');
        }
      });
    });
  });

  // toast for flashed messages
  var toast = document.getElementById('toast');
  if (toast && toast.textContent.trim() !== '') {
    setTimeout(function(){
      toast.classList.add('show');
      setTimeout(function(){ toast.classList.remove('show'); }, 3500);
    }, 300);
  }

  // header border on scroll
  var header = document.querySelector('header');
  if (header) {
    window.addEventListener('scroll', function(){
      header.style.borderBottomColor = window.scrollY > 40 ? 'var(--ink)' : 'var(--line)';
    });
  }
})();
