(() => {
  const normalize = (value) => String(value || "").toLowerCase().replace(/[\s·（）()×*°]/g, "");

  const cards = [...document.querySelectorAll("[data-archive-card]")];
  const search = document.querySelector("[data-archive-search]");
  const filters = [...document.querySelectorAll("[data-archive-category]")];
  let activeCategory = "全部资料";

  const filterCards = () => {
    const query = normalize(search?.value);
    let visible = 0;
    cards.forEach((card) => {
      const categoryMatch = activeCategory === "全部资料" || card.dataset.category === activeCategory;
      const searchMatch = !query || normalize(card.dataset.search).includes(query);
      card.hidden = !(categoryMatch && searchMatch);
      if (!card.hidden) visible += 1;
    });
    const empty = document.querySelector("[data-archive-empty]");
    if (empty) empty.hidden = visible > 0;
  };

  search?.addEventListener("input", filterCards);
  filters.forEach((button) => button.addEventListener("click", () => {
    activeCategory = button.dataset.archiveCategory || "全部资料";
    filters.forEach((item) => item.classList.toggle("active", item === button));
    filterCards();
  }));

  const paneButtons = [...document.querySelectorAll("[data-view-tab]")];
  const panes = [...document.querySelectorAll("[data-view-pane]")];
  const activate = (name, updateUrl = true) => {
    if (!panes.length) return;
    paneButtons.forEach((button) => button.setAttribute("aria-selected", String(button.dataset.viewTab === name)));
    panes.forEach((pane) => { pane.hidden = pane.dataset.viewPane !== name; });
    if (updateUrl) {
      const url = new URL(window.location.href);
      if (name === "training") url.searchParams.set("tab", "training");
      else url.searchParams.delete("tab");
      window.history.replaceState({}, "", url);
    }
  };

  paneButtons.forEach((button) => button.addEventListener("click", () => activate(button.dataset.viewTab || "source")));
  if (panes.length) {
    const requested = new URLSearchParams(window.location.search).get("tab");
    activate(requested === "training" ? "training" : "source", false);
  }

  document.querySelectorAll("[data-training-copy]").forEach((button) => button.addEventListener("click", async () => {
    const target = document.getElementById(button.dataset.trainingCopy);
    if (!target) return;
    try {
      await navigator.clipboard.writeText(target.textContent.trim());
      const previous = button.textContent;
      button.textContent = "已复制";
      setTimeout(() => { button.textContent = previous; }, 1200);
    } catch {
      button.textContent = "请长按话术复制";
    }
  }));
})();
