const CACHE_NAME = 'planner-v1';
const ASSETS = [
    './',
    './index.html',
    './style.css',
    './app.js',
    './manifest.webmanifest',
    './icons/icon-192.png',
    './icons/icon-512.png'
];

self.addEventListener('install',(event)=>{
    event.waitUntil(caches.open(CACHE_NAME).then(cache=> cache.addAll(ASSETS)));
    self.skipWaiting();
});
self.addEventListener('activate',(event)=>{
    event.waitUntil(
        caches.keys().then(keys => Promise.all(keys.map(k => k !== CACHE_NAME && caches.delete(k))))
    );
    self.clients.claim();
});

self.addEventListener('fetch',(event)=> {
    const url = new URL(event.request.url);
    if (ASSETS.includes(url.pathname.replace(self.ServiceWorkerRegistration.scope, './'))){
        event.respondWith(caches.match(event.request));
    } else {
        event.respondWith(
            fetch(event.request).then(resp=> {
                const copy = resp.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
                return resp;
            }).catch(()=> caches.match(event.request))
        );
    }
});