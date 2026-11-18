/**
 * UnboxJoy — Gift Box Builder Frontend Application
 * Interacts with Person 4 Flask API, managing real-time box state,
 * budget progress, sensory balance, packaging selection, and unboxing modal.
 */

// Global State
const state = {
  sessionId: 'session_' + Math.random().toString(36).substring(2, 9),
  targetBudget: 1500,
  products: [],
  activeFilter: 'all',
  box: {
    items: [],
    packagingId: 'eco_kraft',
    targetBudget: 1500
  },
  packagingOptions: [],
  pricing: {
    itemsSubtotal: 0,
    packagingFee: 99,
    taxGst: 5,
    grandTotal: 104,
    remainingBudget: 1396,
    budgetExceeded: false,
    budgetPercentage: 6.9
  },
  sensoryCoverage: {
    sight: 0, sound: 0, smell: 0, taste: 0, touch: 0,
    coveredSenses: [],
    sensoryHarmonyScore: 0
  }
};

// Sense metadata
const SENSE_META = {
  sight: { icon: '👁️', label: 'Sight', bg: 'bg-indigo-50', text: 'text-indigo-700', border: 'border-indigo-200' },
  sound: { icon: '🎵', label: 'Sound', bg: 'bg-cyan-50', text: 'text-cyan-700', border: 'border-cyan-200' },
  smell: { icon: '🌸', label: 'Smell', bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200' },
  taste: { icon: '☕', label: 'Taste', bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
  touch: { icon: '🧸', label: 'Touch', bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' }
};

// Initial API URLs (relative)
const API = {
  health: '/api/health',
  recommendations: '/api/recommendations',
  packaging: '/api/packaging',
  createBox: '/api/box/create',
  boxState: '/api/box/state',
  addItem: '/api/box/items',
  removeItem: (id) => `/api/box/items/${id}`,
  autoAssemble: '/api/box/auto-assemble',
  packagingUpdate: '/api/box/packaging',
  checkout: '/api/cart/checkout'
};

// DOM Elements
const el = {
  productsGrid: document.getElementById('products-grid'),
  filterTabs: document.getElementById('filter-tabs'),
  slotsContainer: document.getElementById('box-slots-container'),
  packagingGrid: document.getElementById('packaging-options-grid'),
  btnAutoAssemble: document.getElementById('btn-auto-assemble'),
  btnResetBox: document.getElementById('btn-reset-box'),
  btnCheckout: document.getElementById('btn-proceed-checkout'),
  checkoutHelper: document.getElementById('checkout-helper-text'),
  overBudgetWarning: document.getElementById('over-budget-warning'),
  overBudgetMsg: document.getElementById('over-budget-msg'),
  // Budget bar
  barSpent: document.getElementById('bar-spent'),
  barTarget: document.getElementById('bar-target'),
  barRemaining: document.getElementById('bar-remaining-badge'),
  progressBar: document.getElementById('budget-progress-bar'),
  // Sensory harmony
  sensoryScore: document.getElementById('sensory-harmony-score'),
  sensoryIndicators: document.getElementById('sensory-indicators'),
  // Pricing card
  priceSubtotal: document.getElementById('price-subtotal'),
  pricePackaging: document.getElementById('price-packaging'),
  priceTax: document.getElementById('price-tax'),
  priceGrandTotal: document.getElementById('price-grand-total'),
  boxCountBadge: document.getElementById('box-item-count-badge'),
  // Card Inputs
  cardTo: document.getElementById('input-recipient-name'),
  cardFrom: document.getElementById('input-sender-name'),
  cardMsg: document.getElementById('input-card-message'),
  // Modal elements
  modal: document.getElementById('unboxing-modal'),
  btnCloseModal: document.getElementById('btn-close-modal'),
  btnUnfastenRibbon: document.getElementById('btn-unfasten-ribbon'),
  boxVisualLid: document.getElementById('box-visual-lid'),
  unboxedReveal: document.getElementById('unboxed-items-reveal'),
  unboxingGrid: document.getElementById('unboxing-reveal-grid'),
  modalCardTo: document.getElementById('modal-card-to'),
  modalCardFrom: document.getElementById('modal-card-from'),
  modalCardMsg: document.getElementById('modal-card-msg'),
  modalOrderId: document.getElementById('modal-order-id'),
  modalDeliveryDate: document.getElementById('modal-delivery-date'),
  modalBrandsSpread: document.getElementById('modal-brands-spread'),
  modalTotalPaid: document.getElementById('modal-total-paid'),
  btnPrintOrder: document.getElementById('btn-print-order'),
  btnConfirmFinish: document.getElementById('btn-confirm-finish')
};

// Initialize Application
async function init() {
  bindEvents();
  try {
    await fetchPackaging();
    await fetchRecommendations();
    await initBoxSession();
  } catch (error) {
    console.warn('API error, falling back to local client state:', error);
    loadFallbackData();
  }
}

// Bind User Interactions
function bindEvents() {
  // Category filter tabs
  el.filterTabs.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    el.filterTabs.querySelectorAll('button').forEach(b => {
      b.classList.remove('bg-slate-900', 'text-white', 'active');
      b.classList.add('bg-slate-100', 'text-slate-700');
    });
    btn.classList.remove('bg-slate-100', 'text-slate-700');
    btn.classList.add('bg-slate-900', 'text-white', 'active');
    state.activeFilter = btn.dataset.filter;
    renderProducts();
  });

  // Auto-assemble button
  el.btnAutoAssemble.addEventListener('click', handleAutoAssemble);

  // Reset button
  el.btnResetBox.addEventListener('click', handleResetBox);

  // Checkout button
  el.btnCheckout.addEventListener('click', handleCheckout);

  // Modal interactions
  el.btnCloseModal.addEventListener('click', () => el.modal.classList.add('hidden'));
  el.btnConfirmFinish.addEventListener('click', () => el.modal.classList.add('hidden'));
  el.btnPrintOrder.addEventListener('click', () => window.print());
  el.btnUnfastenRibbon.addEventListener('click', triggerUnboxingAnimation);

  // Greeting card live sync
  [el.cardTo, el.cardFrom, el.cardMsg].forEach(input => {
    input.addEventListener('input', syncCardData);
  });
}

// Fetch Recommendations
async function fetchRecommendations() {
  const res = await fetch(API.recommendations);
  if (!res.ok) throw new Error('Failed to load recommendations');
  const data = await res.json();
  state.products = data.all_recommendations || [];
  if (data.recipient_profile) {
    state.targetBudget = data.recipient_profile.budget_inr || 1500;
    el.barTarget.textContent = state.targetBudget.toLocaleString();
    if (document.getElementById('ctx-recipient')) {
      document.getElementById('ctx-recipient').textContent = data.recipient_profile.relationship || 'Best Friend';
      document.getElementById('ctx-occasion').textContent = data.recipient_profile.occasion || 'Birthday';
      document.getElementById('ctx-theme').textContent = data.recipient_profile.emotional_theme || 'Nostalgia';
    }
  }
  renderProducts();
}

// Fetch Packaging Options
async function fetchPackaging() {
  const res = await fetch(API.packaging);
  if (!res.ok) throw new Error('Failed to load packaging options');
  const data = await res.json();
  state.packagingOptions = data.packaging_options || [];
  renderPackagingOptions();
}

// Initialize Box Session
async function initBoxSession() {
  const res = await fetch(API.createBox, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: state.sessionId,
      target_budget: state.targetBudget,
      packaging_id: state.box.packagingId
    })
  });
  if (res.ok) {
    const data = await res.json();
    updateBoxState(data.box);
  }
}

// Render Products Grid
function renderProducts() {
  const filtered = state.activeFilter === 'all'
    ? state.products
    : state.products.filter(p => p.category.toLowerCase() === state.activeFilter);

  if (filtered.length === 0) {
    el.productsGrid.innerHTML = `
      <div class="col-span-2 text-center py-12 text-slate-400 bg-white rounded-xl border border-dashed border-slate-200">
        <span class="text-3xl block mb-2">🔍</span>
        <p class="text-sm">No products found in this category.</p>
      </div>`;
    return;
  }

  el.productsGrid.innerHTML = filtered.map(prod => {
    const isAdded = state.box.items.some(item => item.product_id === prod.product_id);
    const meta = SENSE_META[prod.category.toLowerCase()] || SENSE_META.sight;
    const matchPct = Math.round((prod.match_score || 0.85) * 100);

    return `
      <div class="bg-white rounded-xl border border-slate-200/90 shadow-sm overflow-hidden flex flex-col hover:shadow-md transition-all group">
        <div class="relative h-40 bg-slate-100 overflow-hidden">
          <img src="${prod.image_url || 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=500'}"
               alt="${prod.product_name}"
               class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
               onerror="this.src='https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=500'">
          <div class="absolute top-2.5 left-2.5 flex space-x-1.5">
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold ${meta.bg} ${meta.text} border ${meta.border} shadow-xs flex items-center space-x-1">
              <span>${meta.icon}</span>
              <span class="capitalize">${meta.label}</span>
            </span>
          </div>
          <div class="absolute top-2.5 right-2.5">
            <span class="px-2 py-0.5 rounded-full text-[11px] font-bold bg-amber-500 text-slate-950 shadow-xs">
              ${matchPct}% Match
            </span>
          </div>
        </div>

        <div class="p-4 flex-1 flex flex-col justify-between">
          <div>
            <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">${prod.brand}</div>
            <h4 class="text-sm font-bold text-slate-900 mt-0.5 leading-snug line-clamp-1">${prod.product_name}</h4>
            <p class="text-xs text-slate-500 mt-1 line-clamp-2 leading-relaxed">${prod.description}</p>
          </div>

          <div class="mt-3.5 pt-3 border-t border-slate-100 flex items-center justify-between">
            <div>
              <span class="text-base font-extrabold text-slate-900">₹${prod.price}</span>
            </div>
            <button onclick="handleToggleProduct('${prod.product_id}')"
                    class="px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                      isAdded
                        ? 'bg-rose-50 text-rose-600 hover:bg-rose-100 border border-rose-200'
                        : 'bg-slate-900 text-white hover:bg-slate-800 shadow-sm active:scale-95'
                    }">
              ${isAdded ? '✓ Added' : '+ Add to Box'}
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// Render Active Box Slots
function renderBoxSlots() {
  const maxSlots = 5;
  const items = state.box.items || [];
  let html = '';

  for (let i = 0; i < maxSlots; i++) {
    const item = items[i];
    if (item) {
      const meta = SENSE_META[item.category.toLowerCase()] || SENSE_META.sight;
      html += `
        <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between hover:border-slate-300 transition">
          <div class="flex items-center space-x-3 min-w-0">
            <img src="${item.image_url || 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=500'}"
                 class="w-12 h-12 rounded-lg object-cover border border-slate-100 shrink-0"
                 onerror="this.src='https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=500'">
            <div class="min-w-0">
              <div class="flex items-center space-x-1.5">
                <span class="text-[10px] font-bold px-1.5 py-0.2 rounded ${meta.bg} ${meta.text}">
                  ${meta.icon} ${meta.label}
                </span>
                <span class="text-[10px] text-slate-400 font-medium truncate">• ${item.brand}</span>
              </div>
              <h5 class="text-xs font-bold text-slate-900 truncate mt-0.5">${item.product_name}</h5>
              <span class="text-xs font-extrabold text-slate-800">₹${item.price}</span>
            </div>
          </div>
          <button onclick="handleRemoveProduct('${item.product_id}')"
                  class="ml-2 w-7 h-7 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 flex items-center justify-center text-sm font-bold transition shrink-0"
                  title="Remove from box">
            ✕
          </button>
        </div>
      `;
    } else {
      html += `
        <div class="border-2 border-dashed border-slate-200 rounded-xl p-3 flex items-center justify-center text-slate-400 text-xs">
          <span class="text-slate-300 mr-2">➕</span>
          <span>Empty sensory slot (${i + 1} of ${maxSlots})</span>
        </div>
      `;
    }
  }

  el.slotsContainer.innerHTML = html;
  el.boxCountBadge.textContent = `${items.length} / ${maxSlots} Items`;

  // Enable/disable checkout
  const isReady = items.length >= 3;
  el.btnCheckout.disabled = !isReady;
  if (isReady) {
    el.btnCheckout.classList.remove('bg-slate-300', 'text-slate-500', 'cursor-not-allowed');
    el.btnCheckout.classList.add('bg-emerald-600', 'text-white', 'hover:bg-emerald-700', 'shadow-md', 'active:scale-95');
    el.checkoutHelper.textContent = '✓ Ready to preview and order!';
    el.checkoutHelper.classList.add('text-emerald-600', 'font-medium');
  } else {
    el.btnCheckout.classList.add('bg-slate-300', 'text-slate-500', 'cursor-not-allowed');
    el.btnCheckout.classList.remove('bg-emerald-600', 'text-white', 'hover:bg-emerald-700', 'shadow-md', 'active:scale-95');
    el.checkoutHelper.textContent = `Add at least ${3 - items.length} more item(s) to complete your box`;
    el.checkoutHelper.classList.remove('text-emerald-600', 'font-medium');
  }
}

// Render Packaging Options
function renderPackagingOptions() {
  el.packagingGrid.innerHTML = state.packagingOptions.map(opt => {
    const isSelected = opt.id === state.box.packagingId;
    return `
      <div onclick="handleSelectPackaging('${opt.id}')"
           class="p-2.5 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
             isSelected
               ? 'border-amber-500 bg-amber-50/50 shadow-xs ring-1 ring-amber-500'
               : 'border-slate-200 hover:border-slate-300 bg-white'
           }">
        <div>
          <div class="flex items-center justify-between text-xs font-bold text-slate-900">
            <span>${opt.preview_icon || '🎁'} ${opt.name}</span>
            <span class="text-amber-700 font-extrabold">₹${opt.price}</span>
          </div>
          <p class="text-[10px] text-slate-500 mt-1 line-clamp-1">${opt.material}</p>
        </div>
        <div class="mt-2 flex items-center justify-between text-[10px]">
          <span class="text-slate-400 truncate">${opt.sustainability_badge || 'Premium'}</span>
          <span class="text-[11px] font-bold ${isSelected ? 'text-amber-600' : 'text-slate-300'}">
            ${isSelected ? '● Selected' : '○ Select'}
          </span>
        </div>
      </div>
    `;
  }).join('');
}

// Update UI metrics
function updateBoxState(boxData) {
  state.box = boxData;
  state.pricing = boxData.pricing || state.pricing;
  state.sensoryCoverage = boxData.sensory_coverage || state.sensoryCoverage;

  // 1. Update Budget Progress Bar
  const spent = state.pricing.grand_total;
  const target = state.targetBudget;
  const remaining = state.pricing.remaining_budget;
  const pct = Math.min(100, Math.round((spent / target) * 100));

  el.barSpent.textContent = `₹${Math.round(spent).toLocaleString()}`;
  el.barRemaining.textContent = remaining >= 0 ? `₹${Math.round(remaining).toLocaleString()} remaining` : `₹${Math.abs(Math.round(remaining)).toLocaleString()} over budget`;
  el.progressBar.style.width = `${pct}%`;

  if (state.pricing.budget_exceeded) {
    el.progressBar.classList.remove('bg-emerald-500', 'bg-amber-500');
    el.progressBar.classList.add('bg-rose-500');
    el.barRemaining.classList.remove('bg-emerald-500/20', 'text-emerald-400');
    el.barRemaining.classList.add('bg-rose-500/20', 'text-rose-400');
    el.overBudgetWarning.classList.remove('hidden');
    el.overBudgetMsg.textContent = `Your box total exceeds your budget of ₹${target} by ₹${Math.abs(remaining).toFixed(2)}.`;
  } else if (pct >= 85) {
    el.progressBar.classList.remove('bg-emerald-500', 'bg-rose-500');
    el.progressBar.classList.add('bg-amber-500');
    el.barRemaining.classList.remove('bg-rose-500/20', 'text-rose-400');
    el.barRemaining.classList.add('bg-emerald-500/20', 'text-emerald-400');
    el.overBudgetWarning.classList.add('hidden');
  } else {
    el.progressBar.classList.remove('bg-amber-500', 'bg-rose-500');
    el.progressBar.classList.add('bg-emerald-500');
    el.barRemaining.classList.remove('bg-rose-500/20', 'text-rose-400');
    el.barRemaining.classList.add('bg-emerald-500/20', 'text-emerald-400');
    el.overBudgetWarning.classList.add('hidden');
  }

  // 2. Update Sensory Harmony
  const harmony = Math.round(state.sensoryCoverage.sensory_harmony_score || 0);
  el.sensoryScore.textContent = `${harmony}% Balanced (${state.sensoryCoverage.covered_senses.length}/5 Senses)`;

  Object.keys(SENSE_META).forEach(sense => {
    const badge = el.sensoryIndicators.querySelector(`[data-sense="${sense}"]`);
    if (badge) {
      const isCovered = (state.sensoryCoverage[sense] || 0) > 0;
      if (isCovered) {
        badge.classList.remove('bg-slate-800', 'text-slate-500', 'border-slate-700');
        badge.classList.add('bg-amber-400', 'text-slate-950', 'border-amber-300', 'font-bold');
      } else {
        badge.classList.add('bg-slate-800', 'text-slate-500', 'border-slate-700');
        badge.classList.remove('bg-amber-400', 'text-slate-950', 'border-amber-300', 'font-bold');
      }
    }
  });

  // 3. Update Financial Breakdown
  el.priceSubtotal.textContent = `₹${state.pricing.items_subtotal}`;
  el.pricePackaging.textContent = `₹${state.pricing.packaging_fee}`;
  el.priceTax.textContent = `₹${state.pricing.tax_gst}`;
  el.priceGrandTotal.textContent = `₹${state.pricing.grand_total}`;

  // 4. Re-render Slots & Catalog Badges
  renderBoxSlots();
  renderProducts();
  renderPackagingOptions();
}

// Add/Remove Handler
window.handleToggleProduct = async function(productId) {
  const isAdded = state.box.items.some(item => item.product_id === productId);
  if (isAdded) {
    await handleRemoveProduct(productId);
  } else {
    await handleAddProduct(productId);
  }
};

window.handleAddProduct = async function(productId) {
  try {
    const res = await fetch(API.addItem, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: state.sessionId,
        product_id: productId,
        strict_budget: false
      })
    });
    const data = await res.json();
    if (res.ok) {
      updateBoxState(data.box);
    } else {
      alert(data.error || data.message);
    }
  } catch (error) {
    console.error('Add product error:', error);
  }
};

window.handleRemoveProduct = async function(productId) {
  try {
    const res = await fetch(API.removeItem(productId) + `?session_id=${state.sessionId}`, {
      method: 'DELETE'
    });
    const data = await res.json();
    if (res.ok) {
      updateBoxState(data.box);
    }
  } catch (error) {
    console.error('Remove product error:', error);
  }
};

window.handleSelectPackaging = async function(packagingId) {
  state.box.packagingId = packagingId;
  try {
    const res = await fetch(API.packagingUpdate, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: state.sessionId,
        packaging_id: packagingId
      })
    });
    if (res.ok) {
      const data = await res.json();
      updateBoxState(data.box);
    }
  } catch (error) {
    console.error('Packaging update error:', error);
  }
};

async function handleAutoAssemble() {
  try {
    el.btnAutoAssemble.disabled = true;
    el.btnAutoAssemble.innerHTML = '<span>⏳</span><span>Assembling...</span>';
    const res = await fetch(API.autoAssemble, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: state.sessionId,
        target_budget: state.targetBudget,
        packaging_id: state.box.packagingId,
        item_count: 4
      })
    });
    const data = await res.json();
    if (res.ok && data.box) {
      updateBoxState(data.box);
    } else {
      alert(data.message || 'Auto-assembly completed with partial items.');
    }
  } catch (error) {
    console.error('Auto-assemble error:', error);
  } finally {
    el.btnAutoAssemble.disabled = false;
    el.btnAutoAssemble.innerHTML = '<span>⚡</span><span>Auto-Assemble Box</span>';
  }
}

async function handleResetBox() {
  if (!confirm('Are you sure you want to empty your current gift box?')) return;
  await initBoxSession();
}

function syncCardData() {
  // Sync live preview
}

async function handleCheckout() {
  try {
    el.btnCheckout.disabled = true;
    el.btnCheckout.textContent = 'Generating Unboxing Experience...';

    const res = await fetch(API.checkout, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: state.sessionId,
        recipient_name: el.cardTo.value.trim() || 'Best Friend',
        sender_name: el.cardFrom.value.trim() || 'A Thoughtful Friend',
        occasion: 'Birthday Celebration',
        personalized_message: el.cardMsg.value.trim()
      })
    });

    const data = await res.json();
    if (res.ok && data.order) {
      populateOrderModal(data.order);
      el.modal.classList.remove('hidden');
    } else {
      alert(data.error || 'Failed to place order.');
    }
  } catch (error) {
    console.error('Checkout error:', error);
  } finally {
    el.btnCheckout.disabled = false;
    el.btnCheckout.innerHTML = '<span>🎁</span><span>Preview & Checkout Box</span>';
  }
}

function populateOrderModal(order) {
  // Reset lid animation
  el.boxVisualLid.classList.remove('lid-open');
  el.boxVisualLid.style.display = 'block';
  el.unboxedReveal.classList.add('hidden');
  el.btnUnfastenRibbon.classList.remove('hidden');

  // Set packaging style
  const pack = order.packaging;
  document.getElementById('unboxing-box-name').textContent = pack.name;
  document.getElementById('box-lid-graphic').style.backgroundColor = pack.color_theme || '#D2B48C';

  // Greeting card text
  el.modalCardTo.textContent = order.recipient_details.name;
  el.modalCardFrom.textContent = order.sender_details.name;
  el.modalCardMsg.textContent = `"${order.greeting_card.message}"`;

  // Receipt details
  el.modalOrderId.textContent = order.order_id;
  el.modalDeliveryDate.textContent = order.estimated_delivery;
  el.modalBrandsSpread.textContent = order.unboxing_experience.brands_curated.join(', ');
  el.modalTotalPaid.textContent = `₹${order.financial_summary.grand_total}`;

  // Populate revealed items
  el.unboxingGrid.innerHTML = order.unboxing_experience.reveal_sequence.map(item => {
    const meta = SENSE_META[item.category.toLowerCase()] || SENSE_META.sight;
    return `
      <div class="reveal-item bg-white p-3 rounded-xl border border-slate-200 shadow-xs flex items-center space-x-3">
        <img src="${item.image_url || 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=500'}"
             class="w-12 h-12 rounded-lg object-cover border border-slate-100 shrink-0"
             onerror="this.src='https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=500'">
        <div class="min-w-0">
          <span class="text-[10px] font-bold px-1.5 py-0.2 rounded ${meta.bg} ${meta.text}">
            ${meta.icon} ${item.sensory_highlight}
          </span>
          <h5 class="text-xs font-bold text-slate-900 truncate mt-0.5">${item.product_name}</h5>
          <span class="text-xs font-bold text-slate-500">${item.brand} • ₹${item.price}</span>
        </div>
      </div>
    `;
  }).join('');
}

function triggerUnboxingAnimation() {
  el.boxVisualLid.classList.add('lid-open');
  setTimeout(() => {
    el.boxVisualLid.style.display = 'none';
    el.unboxedReveal.classList.remove('hidden');
  }, 500);
}

// Fallback data if offline
function loadFallbackData() {
  state.products = [
    { product_id: 'SIGHT001', product_name: 'Wooden Photo Frame', brand: 'Chumbak', category: 'sight', price: 399, match_score: 0.94, description: 'Artistic photo frame to hold cherished memories.' },
    { product_id: 'SOUND001', product_name: 'Stone 352 Speaker', brand: 'boAt', category: 'sound', price: 499, match_score: 0.85, description: 'Portable wireless acoustics.' },
    { product_id: 'SMELL001', product_name: 'Lavender Candle', brand: 'Ekam', category: 'smell', price: 349, match_score: 0.93, description: 'Soothing French lavender botanical candle.' },
    { product_id: 'TASTE001', product_name: 'Artisan Dark Chocolate', brand: 'Mason & Co', category: 'taste', price: 299, match_score: 0.89, description: 'Organic sea salt bean-to-bar chocolate.' },
    { product_id: 'TOUCH001', product_name: 'Hardbound Journal', brand: 'Odd Giraffe', category: 'touch', price: 299, match_score: 0.92, description: 'Recycled paper tactile journal.' }
  ];
  state.packagingOptions = [
    { id: 'eco_kraft', name: 'Eco-Friendly Kraft Keepsake', price: 99, material: 'Recycled Kraft Board', preview_icon: '📦🌱' },
    { id: 'midnight_luxe', name: 'Midnight Matte Luxe', price: 199, material: 'Soft-Touch Matte & Gold Foil', preview_icon: '✨🎁' },
    { id: 'pastel_blossom', name: 'Pastel Blossom Celebration', price: 149, material: 'Blush Finish & Satin Ribbon', preview_icon: '🌸🎀' },
    { id: 'velvet_chest', name: 'Minimalist Velvet Chest', price: 249, material: 'Wooden Core & Velvet Lining', preview_icon: '👑💎' }
  ];
  renderProducts();
  renderBoxSlots();
  renderPackagingOptions();
}

// Start
document.addEventListener('DOMContentLoaded', init);
