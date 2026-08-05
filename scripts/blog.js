(() => {
  "use strict";

  const filter = document.getElementById("post-filter");
  const list = document.getElementById("post-list");
  const count = document.getElementById("visible-post-count");
  const empty = document.getElementById("no-post-results");
  if (!filter || !list) return;

  const items = [...list.children];
  const applyFilter = () => {
    const query = filter.value.trim().toLowerCase();
    let visible = 0;
    items.forEach((item) => {
      const matches = !query || (item.dataset.search || item.textContent.toLowerCase()).includes(query);
      item.hidden = !matches;
      if (matches) visible += 1;
    });
    if (count) count.textContent = String(visible);
    if (empty) empty.hidden = visible !== 0;
  };

  filter.addEventListener("input", applyFilter);
})();
