// Legacy reference pages remain no-JavaScript fallbacks. With JavaScript,
// carry existing routes and both explicit and automatic heading bookmarks
// into the field guide, including when the site is hosted under a subpath.
(() => {
  const script = document.querySelector('script[src$="/reader-navigation.js"]');
  if (!script) return;
  const base = new URL('../../', script.src);
  const relative = location.pathname.slice(base.pathname.length).replace(/index\.html$/, '');
  const routes = __GUIDE_ROUTES__;
  const overviewHashes = new Set(['#hay-description-specification', '#interpretation-conventions', '#known-source-issues', '#field-reference', '#source-front-matter']);
  function redirect() {
    if (relative === 'technical/' || (relative === '' && overviewHashes.has(location.hash))) {
      const destination = new URL('guidance/specification/', base);
      destination.hash = location.hash;
      location.replace(destination.href);
      return;
    }
    const route = routes[relative];
    if (!route) return;
    let anchor;
    try { anchor = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    // Unknown fragments must not resolve through Object.prototype properties.
    const sourceKey = (id) => Object.prototype.hasOwnProperty.call(route.anchors, id)
      ? route.anchors[id] : undefined;
    let key = sourceKey(anchor);
    if (anchor && !key) {
      // MkDocs also creates automatic heading IDs. Find the preceding stable
      // explicit source anchor, preserving bookmarks copied from those headings.
      const target = document.getElementById(anchor);
      if (!target) return; // Unknown bookmarks retain the original fallback page.
      for (const source of document.querySelectorAll('a[id^="node-sections-"]')) {
        if (source === target || source.compareDocumentPosition(target) & Node.DOCUMENT_POSITION_FOLLOWING)
          key = sourceKey(source.id) || key;
      }
    }
    if (!key) key = route.root;
    const destination = new URL(route.guide, base);
    destination.hash = encodeURIComponent(key);
    location.replace(destination.href);
  }
  redirect();
  window.addEventListener('hashchange', redirect);
})();
