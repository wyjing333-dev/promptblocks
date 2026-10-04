// PromptBlocks Service Worker - PWA Offline Support
const CACHE_NAME = 'promptblocks-v3';
const ASSETS = [
  './',
  './index.html',
  './manifest.json'
];

// Install - cache core assets
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(ASSETS).catch(function(err) {
        console.log('Cache some assets failed:', err);
      });
    })
  );
  self.skipWaiting();
});

// Activate - clean old caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.filter(function(name) { return name !== CACHE_NAME; })
          .map(function(name) { return caches.delete(name); })
      );
    })
  );
  self.clients.claim();
});

// Fetch - network-first for HTML, cache-first for assets
self.addEventListener('fetch', function(event) {
  if (event.request.method !== 'GET') return;
  
  var url = new URL(event.request.url);
  if (url.origin !== location.origin) return;
  
  var isHTML = event.request.destination === 'document' || url.pathname.endsWith('.html') || url.pathname === '/' || url.pathname === '';
  
  if (isHTML) {
    // Network-first for HTML: always try network, fall back to cache
    event.respondWith(
      fetch(event.request).then(function(response) {
        if (response && response.status === 200) {
          var clone = response.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(event.request, clone);
          });
        }
        return response;
      }).catch(function() {
        return caches.match(event.request).then(function(cached) {
          return cached || caches.match('./index.html');
        });
      })
    );
  } else {
    // Cache-first for static assets (JS, CSS, JSON, images)
    event.respondWith(
      caches.match(event.request).then(function(cached) {
        if (cached) {
          fetch(event.request).then(function(response) {
            if (response && response.status === 200) {
              var clone = response.clone();
              caches.open(CACHE_NAME).then(function(cache) {
                cache.put(event.request, clone);
              });
            }
          }).catch(function() {});
          return cached;
        }
        return fetch(event.request).then(function(response) {
          if (!response || response.status !== 200) return response;
          var clone = response.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(event.request, clone);
          });
          return response;
        });
      })
    );
  }
});
