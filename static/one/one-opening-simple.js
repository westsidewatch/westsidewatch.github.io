/* ONE opening: keep the 66 books in their natural vertical order. */
(() => {
  "use strict";
  const list = document.getElementById("cover-books");
  const data = window.ONE_DATA;
  if (!list || !data?.books) return;

  const open = item => {
    const book = data.books.find(entry => entry[0] === Number(item?.dataset?.book));
    if (book && typeof window.selectCoverBook === "function") window.selectCoverBook(book);
  };

  const resetRailStyles = () => {
    list.classList.add("is-settled");
    list.querySelectorAll(".cover-book").forEach(item => {
      item.style.removeProperty("--rail-y");
      item.style.removeProperty("--rail-scale");
      item.style.removeProperty("--rail-opacity");
      item.classList.remove("rail-near");
    });
  };

  requestAnimationFrame(resetRailStyles);
  new MutationObserver(resetRailStyles).observe(list,{childList:true});

  list.addEventListener("click", event => {
    const item = event.target.closest(".cover-book");
    if (!item || !list.contains(item)) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    open(item);
  }, true);

  list.addEventListener("wheel", event => event.stopImmediatePropagation(), true);
  ["pointerdown","pointermove","pointerup","pointercancel"].forEach(type => {
    list.addEventListener(type, event => event.stopImmediatePropagation(), true);
  });
})();
