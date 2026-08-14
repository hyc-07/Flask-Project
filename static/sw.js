// Service Worker - 聊天室 PWA
const CACHE_NAME = 'chat-app-v1';
const STATIC_CACHE = 'chat-static-v1';

// 需要预缓存的静态资源
const PRECACHE_URLS = [
  '/static/manifest.json',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/static/icons/apple-touch-icon.png'
];

// 安装阶段：预缓存静态资源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

// 激活阶段：清理旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME && name !== STATIC_CACHE)
          .map((name) => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// 请求拦截
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // 只处理 GET 请求
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // WebSocket 连接不处理
  if (request.url.includes('socket.io') || url.protocol === 'ws:' || url.protocol === 'wss:') {
    return;
  }

  // 静态资源：缓存优先策略
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((response) => {
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(STATIC_CACHE).then((cache) => cache.put(request, responseClone));
          }
          return response;
        }).catch(() => cached);
      })
    );
    return;
  }

  // 页面请求：网络优先策略，失败时回退到缓存
  if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
          }
          return response;
        })
        .catch(() => {
          return caches.match(request).then((cached) => {
            if (cached) return cached;
            // 返回离线提示
            return new Response(
              `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>离线</title><style>body{font-family:-apple-system,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;background:linear-gradient(135deg,#11998e,#38ef7d);color:#333}.card{background:white;padding:40px;border-radius:16px;text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.15)}h2{margin:0 0 12px}p{color:#666;margin:0}</style></head><body><div class="card"><h2>📡 网络连接已断开</h2><p>请检查网络后重试</p></div></body></html>`,
              { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
            );
          });
        })
    );
    return;
  }

  // 其他请求：默认网络优先
  event.respondWith(
    fetch(request)
      .then((response) => {
        if (response && response.status === 200 && request.url.startsWith(self.location.origin)) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
        }
        return response;
      })
      .catch(() => caches.match(request))
  );
});
