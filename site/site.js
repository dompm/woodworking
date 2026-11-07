(() => {
  const viewer = document.querySelector('.viewer');
  const links = [...document.querySelectorAll('[data-lightbox]')];
  if (!viewer || !links.length) return;
  const holder = viewer.querySelector('[data-viewer-image]');
  const caption = viewer.querySelector('[data-caption]');
  let current = 0;
  function show(index) {
    current = (index + links.length) % links.length;
    const link = links[current];
    const image = new Image();
    image.src = link.href;
    image.alt = link.dataset.caption || '';
    holder.replaceChildren(image);
    caption.textContent = link.dataset.caption || '';
  }
  links.forEach((link, index) => link.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    show(index);
    viewer.showModal();
  }));
  viewer.querySelector('[data-prev]').addEventListener('click', () => show(current - 1));
  viewer.querySelector('[data-next]').addEventListener('click', () => show(current + 1));
  viewer.querySelector('[data-close]').addEventListener('click', () => viewer.close());
  viewer.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
  });
})();
