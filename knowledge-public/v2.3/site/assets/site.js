(() => {
  const normalize = (value) => String(value || "").toLowerCase().replace(/[\s·（）()×*°]/g, "");
  const tokens = (value) => normalize(value).split(/[，。；、/]/).filter(Boolean);
  const score = (item, query) => {
    const needle = normalize(query);
    if (!needle) return 0;
    const name = normalize(item.name);
    const aliases = normalize((item.aliases || []).join(" "));
    const category = normalize(item.category);
    const body = normalize([item.intro, item.price, ...(item.keywords || [])].join(" "));
    let value = 0;
    if (name === needle) value += 120;
    if (name.includes(needle) || needle.includes(name)) value += 80;
    if (aliases.includes(needle)) value += 60;
    if (category.includes(needle)) value += 35;
    if (body.includes(needle)) value += 25;
    const intentWords = ["多少钱", "价格", "怎么吃", "怎么用", "哪里来的", "是什么", "怎么样"];
    const coreNeedle = intentWords.reduce((text, word) => text.replace(normalize(word), ""), needle);
    if (coreNeedle.length >= 2 && coreNeedle !== needle) {
      if (name.includes(coreNeedle) || aliases.includes(coreNeedle)) value += 70;
      else if (category.includes(coreNeedle) || body.includes(coreNeedle)) value += 30;
      if (intentWords.some((word) => needle.includes(normalize(word)) && body.includes(normalize(word)))) value += 15;
    }
    for (const token of tokens(query)) {
      if (name.includes(token)) value += 18;
      if (aliases.includes(token)) value += 12;
      if (body.includes(token)) value += 6;
    }
    return value;
  };

  const renderSearch = (input, target) => {
    const query = input.value.trim();
    if (!target) return;
    if (!query) {
      target.innerHTML = '<p class="search-hint">输入产品名、别名或问题开始查询。</p>';
      return;
    }
    const results = (window.JIYANGJIA_SEARCH_INDEX || [])
      .map((item) => ({ item, score: score(item, query) }))
      .filter((entry) => entry.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 8);
    target.innerHTML = results.length
      ? results.map(({ item }) => `<a class="search-hit" href="${item.url}"><span>${item.type} · ${item.category}</span><strong>${item.name}</strong><p>${item.intro}</p>${item.price ? `<small>${item.price}</small>` : ""}</a>`).join("")
      : '<div class="empty-state compact"><strong>没有找到匹配资料</strong><p>换一个产品名，或直接查看十个知识板块。</p></div>';
  };

  document.querySelectorAll("[data-site-search]").forEach((input) => {
    const scope = input.closest("section") || document;
    const target = scope.querySelector("[data-search-results]");
    const run = () => renderSearch(input, target);
    input.addEventListener("input", run);
    run();
    document.querySelectorAll("[data-query]").forEach((button) => button.addEventListener("click", () => {
      input.value = button.dataset.query || "";
      run();
      input.focus();
    }));
  });

  document.querySelectorAll("[data-card-filter]").forEach((input) => {
    const grid = input.closest(".content-wrap")?.querySelector("[data-filter-grid]");
    input.addEventListener("input", () => {
      const needle = normalize(input.value);
      grid?.querySelectorAll("[data-search-card]").forEach((card) => {
        card.hidden = Boolean(needle) && !normalize(card.dataset.search).includes(needle);
      });
    });
  });

  document.querySelectorAll("[data-copy-target]").forEach((button) => button.addEventListener("click", async () => {
    const target = document.getElementById(button.dataset.copyTarget);
    if (!target) return;
    try {
      await navigator.clipboard.writeText(target.textContent.trim());
      const old = button.textContent;
      button.textContent = "已复制";
      setTimeout(() => { button.textContent = old; }, 1200);
    } catch {
      button.textContent = "请长按话术复制";
    }
  }));
})();
