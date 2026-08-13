/* Direct selection for the simplified ONE opening. */
(() => {
  "use strict";
  const list = document.getElementById("cover-books");
  const data = window.ONE_DATA;
  if (!list || !data?.books) return;

  const open = item => {
    const book = data.books.find(entry => entry[0] === Number(item?.dataset?.book));
    if (book && typeof window.selectCoverBook === "function") window.selectCoverBook(book);
  };

  list.addEventListener("click", event => {
    const item = event.target.closest(".cover-book");
    if (!item || !list.contains(item)) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    open(item);
  }, true);

  list.addEventListener("wheel", event => event.stopImmediatePropagation(), true);
  ["pointerdown","pointermove","pointerup","pointercancel"].forEach(type => {
    list.addEventListener(type, event => {
      if (event.target.closest(".cover-book")) event.stopImmediatePropagation();
    }, true);
  });
})();
