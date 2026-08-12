(() => {
  if (window.self !== window.top || new URLSearchParams(window.location.search).has("embedded")) {
    document.documentElement.classList.add("jyj-embedded");
  }
})();
