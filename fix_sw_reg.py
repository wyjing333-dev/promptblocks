"""Fix SW registration to unregister old SWs first"""
import re

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_sw = """// ===== PWA Service Worker =====
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('sw.js').then(function(reg) {
      console.log('SW registered: ' + reg.scope);
    }).catch(function(err) {
      console.log('SW registration failed: ' + err);
    });
  });
}"""

new_sw = """// ===== PWA Service Worker =====
if ('serviceWorker' in navigator) {
  // Unregister any old service workers first, then register fresh
  navigator.serviceWorker.getRegistrations().then(function(regs) {
    regs.forEach(function(reg) { reg.unregister(); });
    navigator.serviceWorker.register('sw.js?v=2').then(function(reg) {
      console.log('SW registered: ' + reg.scope);
    }).catch(function(err) {
      console.log('SW registration failed: ' + err);
    });
  });
}"""

if old_sw in content:
    content = content.replace(old_sw, new_sw, 1)
    with open(r'D:\jieyuexingchen\promptblocks\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SW registration code replaced successfully')
else:
    print('Old SW code not found - checking if already replaced')
    if 'getRegistrations' in content:
        print('Already replaced')
    else:
        print('ERROR: Could not find old SW code')
