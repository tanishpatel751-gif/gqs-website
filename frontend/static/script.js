console.log("Welcome to GQS!");

// Global state
let products = [];
let index = 0;

// ================= FETCH PRODUCTS =================
async function loadProducts() {
  try {
    const response = await fetch('/api/products');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();

    products = data.map(p => ({
      name: p.name,
      img: `/static/${p.img}`,
      descript: p.descript,
      price: Number(p.price) || 0
    }));

    console.debug('Loaded products from API:', products);

  } catch (error) {
    console.error("Error fetching products:", error);
  }
}

// ================= RENDER CAROUSEL =================
function renderProducts() {
  const trackEl = document.getElementById("carouselTrack");
  if (!trackEl) return;

  trackEl.innerHTML = "";

  products.forEach((p, idx) => {
    trackEl.innerHTML += `
      <div class="carousel-item" data-index="${idx}">
        <img src="${p.img}" alt="${p.name}">
        <p>${p.name}</p>
        <p>${p.descript}</p>
        <p>$${p.price.toFixed(2)}</p>
      </div>
    `;
  });
}

// ================= CAROUSEL LOGIC =================
function getItems() {
  return Array.from(document.querySelectorAll(".carousel-item"));
}

function getItemWidth() {
  const item = getItems()[0];
  if (!item) return 0;

  const styles = getComputedStyle(item);
  return item.getBoundingClientRect().width +
         parseFloat(styles.marginLeft) +
         parseFloat(styles.marginRight);
}

function updateCarousel() {
  const trackEl = document.getElementById("carouselTrack");
  if (!trackEl) return;

  const items = getItems();
  const maxIndex = Math.max(items.length - 1, 0);

  index = Math.max(0, Math.min(index, maxIndex));
  trackEl.style.transform = `translateX(-${index * getItemWidth()}px)`;
}

// ================= PRODUCT DETAILS PAGE =================
function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

function productHTML(p) {
  return `
    <div class="product-details">
      <img src="${p.img}" alt="${p.name}">
      <h3>${p.name}</h3>
      <p>${p.descript}</p>
      <p>$${p.price.toFixed(2)}</p>
      <a class="contact-btn" href="/contact">Contact Us</a>
    </div>
  `;
}

function renderProductDetails() {
  const detailsEl = document.getElementById("product-details");
  if (!detailsEl) return;

  const idx = Number(getQueryParam("index"));
  if (Number.isNaN(idx) || idx < 0 || idx >= products.length) {
    detailsEl.innerHTML = "<p>Product not found.</p>";
    console.debug('Invalid index for product details:', idx, 'products.length=', products.length);
    return;
  }

  console.debug('Rendering product details for index', idx, products[idx]);
  detailsEl.innerHTML = productHTML(products[idx]);
}

// ================= APP INIT =================
document.addEventListener("DOMContentLoaded", async () => {

  await loadProducts();  // 🔥 Wait for database data

  // Carousel page
  if (document.getElementById("carouselTrack")) {
    renderProducts();
    updateCarousel();

    document.querySelector(".next")?.addEventListener("click", () => {
      index++;
      updateCarousel();
    });

    document.querySelector(".prev")?.addEventListener("click", () => {
      index--;
      updateCarousel();
    });

    document.getElementById("carouselTrack").addEventListener("click", (e) => {
      const item = e.target.closest(".carousel-item");
      if (!item) return;
      window.location.href = `/proddets?index=${item.dataset.index}`;
    });

    window.addEventListener("resize", updateCarousel);
  }

  // Product details page
  renderProductDetails();
});

/*console.log("Welcome to GQS!");

let products = [];
let index = 0;

async function loadProducts() {
  try {
    const response = await fetch('/api/products');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();

    products = data.map(p => ({
      name: p.name || "Unnamed Product",
      img: `/static/${p.img || "placeholder.jpg"}`,
      descript: p.descript || "No description available.",
      price: Number(p.price) || 0
    }));

  } catch (error) {
    console.error("Error fetching products:", error);
  }
}

function renderProducts() {
  const trackEl = document.getElementById("carouselTrack");
  if (!trackEl) return;

  trackEl.innerHTML = "";

  products.forEach((p, idx) => {
    trackEl.innerHTML += `
      <div class="carousel-item" data-index="${idx}">
        <img src="${p.img}" alt="${p.name}">
        <p>${p.name}</p>
        <p>${p.descript}</p>
        <p>$${p.price.toFixed(2)}</p>
      </div>
    `;
  });
}

function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

function productHTML(p) {
  return `
    <div class="product-details">
      <img src="${p.img}" alt="${p.name}">
      <h3>${p.name}</h3>
      <p>${p.descript}</p>
      <p>$${p.price.toFixed(2)}</p>
      <a class="contact-btn" href="contact.html">Contact Us</a>
    </div>
  `;
}

function renderProductDetails() {
  const detailsEl = document.getElementById("product-details");
  if (!detailsEl) return;

  const idx = Number(getQueryParam("index"));
  if (Number.isNaN(idx) || idx < 0 || idx >= products.length) {
    detailsEl.innerHTML = "<p>Product not found.</p>";
    return;
  }

  detailsEl.innerHTML = productHTML(products[idx]);
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadProducts();
  renderProducts();
  renderProductDetails();
});
*/