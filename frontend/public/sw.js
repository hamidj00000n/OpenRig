const CACHE_NAME = "openrig-shell-v1";
const APP_SHELL = ["/", "/index.html", "/manifest.webmanifest", "/openrig-config.js"];
self.addEventListener("install", event => { event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL))); self.skipWaiting(); });
self.addEventListener("activate", event => { event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))))); self.clients.claim(); });
self.addEventListener("fetch", event => { const req=event.request; const url=new URL(req.url); if(req.method!=="GET"||url.origin!==self.location.origin||url.pathname.startsWith("/api/")) return; event.respondWith(fetch(req).then(res=>{if(res.ok&&res.type==="basic"){const copy=res.clone();caches.open(CACHE_NAME).then(cache=>cache.put(req,copy));}return res;}).catch(async()=>{const cached=await caches.match(req);return cached||(req.mode==="navigate"?caches.match("/index.html"):Response.error());})); });
