// Carry existing overview bookmarks to the relocated technical overview.
(() => {
  const home = document.querySelector('[data-technical-overview]');
  const legacy = new Set(['#hay-description-specification', '#interpretation-conventions', '#known-source-issues', '#field-reference', '#source-front-matter']);
  function forwardOverviewBookmark() {
    if (!home || !legacy.has(window.location.hash)) return;
    const destination = new URL(home.dataset.technicalOverview, window.location.href);
    destination.hash = window.location.hash;
    window.location.replace(destination.href);
  }
  forwardOverviewBookmark();
  window.addEventListener("hashchange", forwardOverviewBookmark);
})();
