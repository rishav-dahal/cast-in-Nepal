/**
 * Interactive Application Controller for Castes, Surnames & Gotras of Nepal
 * Handles search, multi-dimensional filters, views, sagotra matching, and bookmarks.
 */

(function () {
  'use strict';

  // State
  const state = {
    searchQuery: '',
    selectedCategory: 'all',
    selectedCommunity: 'all',
    selectedGotra: 'all',
    selectedRegion: 'all',
    sortBy: 'surname-asc',
    viewMode: 'grid', // 'grid' | 'table' | 'sagotra' | 'checker' | 'insights'
    page: 1,
    pageSize: 36,
    favorites: new Set(JSON.parse(localStorage.getItem('nepal_surnames_favs') || '[]')),
    theme: localStorage.getItem('nepal_surnames_theme') || 'dark',
    activeSurname: null
  };

  // Sagotra Collision Checker State
  const checkerState = {
    partnerAId: 1,
    partnerAGotra: '',
    partnerAMamaGotra: '',
    partnerBId: 575,
    partnerBGotra: '',
    partnerBMamaGotra: '',
    evaluated: true
  };

  // DOM Elements Cache
  const DOM = {
    themeToggleBtn: document.getElementById('themeToggleBtn'),
    themeIcon: document.getElementById('themeIcon'),
    favDrawerOpenBtn: document.getElementById('favDrawerOpenBtn'),
    favBadgeCount: document.getElementById('favBadgeCount'),
    searchInput: document.getElementById('searchInput'),
    searchClearBtn: document.getElementById('searchClearBtn'),
    statTotalCount: document.getElementById('statTotalCount'),
    statCatCount: document.getElementById('statCatCount'),
    statGotraCount: document.getElementById('statGotraCount'),
    statRegionCount: document.getElementById('statRegionCount'),
    categoryFilterBar: document.getElementById('categoryFilterBar'),
    communityFilterSelect: document.getElementById('communityFilterSelect'),
    gotraFilterSelect: document.getElementById('gotraFilterSelect'),
    regionFilterSelect: document.getElementById('regionFilterSelect'),
    sortBySelect: document.getElementById('sortBySelect'),
    resetFiltersBtn: document.getElementById('resetFiltersBtn'),
    resultsCount: document.getElementById('resultsCount'),
    viewGridBtn: document.getElementById('viewGridBtn'),
    viewTableBtn: document.getElementById('viewTableBtn'),
    viewSagotraBtn: document.getElementById('viewSagotraBtn'),
    viewCheckerBtn: document.getElementById('viewCheckerBtn'),
    viewInsightsBtn: document.getElementById('viewInsightsBtn'),
    contentSection: document.getElementById('contentSection'),
    paginationContainer: document.getElementById('paginationContainer'),
    loadMoreBtn: document.getElementById('loadMoreBtn'),
    modalOverlay: document.getElementById('detailModal'),
    modalCloseBtn: document.getElementById('modalCloseBtn'),
    modalContent: document.getElementById('modalContent'),
    drawerOverlay: document.getElementById('favDrawerOverlay'),
    drawerCloseBtn: document.getElementById('drawerCloseBtn'),
    drawerList: document.getElementById('drawerList'),
    clearFavsBtn: document.getElementById('clearFavsBtn'),
    toastContainer: document.getElementById('toastContainer')
  };

  // Category Colors / Badges
  const CATEGORY_CONFIG = {
    'Khas-Arya': { class: 'badge-khas', color: '#f59e0b' },
    'Newar': { class: 'badge-newar', color: '#ef4444' },
    'Indigenous Janajati': { class: 'badge-janajati', color: '#10b981' },
    'Madhesi / Terai': { class: 'badge-madhesi', color: '#3b82f6' },
    'Dalit': { class: 'badge-dalit', color: '#ec4899' },
    'Muslim': { class: 'badge-muslim', color: '#14b8a6' }
  };

  /**
   * Initialize Application
   */
  function init() {
    initTheme();
    populateStats();
    populateFilterDropdowns();
    renderCategoryFilterBar();
    updateFavBadge();
    bindEvents();
    render();
  }

  /**
   * Theme Management
   */
  function initTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    updateThemeIcon();
  }

  function toggleTheme() {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('nepal_surnames_theme', state.theme);
    updateThemeIcon();
    showToast(`Switched to ${state.theme === 'dark' ? 'Dark' : 'Light'} Mode`);
  }

  function updateThemeIcon() {
    if (DOM.themeIcon) {
      DOM.themeIcon.innerHTML = state.theme === 'dark'
        ? `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`
        : `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    }
  }

  function getFavIconSvg(isFav) {
    if (isFav) {
      return `<svg width="14" height="14" viewBox="0 0 24 24" fill="#f43f5e" stroke="#f43f5e" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`;
    }
    return `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`;
  }

  /**
   * Stats Population
   */
  function populateStats() {
    if (!window.CASTE_DATABASE) return;

    const totalSurnames = CASTE_DATABASE.length;
    const categories = new Set(CASTE_DATABASE.map(item => item.category)).size;
    const gotras = new Set(CASTE_DATABASE.map(item => item.gotra)).size;

    if (DOM.statTotalCount) DOM.statTotalCount.textContent = totalSurnames;
    if (DOM.statCatCount) DOM.statCatCount.textContent = categories;
    if (DOM.statGotraCount) DOM.statGotraCount.textContent = gotras;
    if (DOM.statRegionCount) DOM.statRegionCount.textContent = '7';
  }

  /**
   * Populate Dynamic Filter Dropdowns
   */
  function populateFilterDropdowns() {
    if (!window.CASTE_DATABASE) return;

    // Unique Communities
    const communities = [...new Set(CASTE_DATABASE.map(item => item.community))].sort();
    if (DOM.communityFilterSelect) {
      DOM.communityFilterSelect.innerHTML = '<option value="all">All Communities</option>' +
        communities.map(c => `<option value="${c}">${c}</option>`).join('');
    }

    // Unique Gotras
    const gotras = [...new Set(CASTE_DATABASE.map(item => item.gotra))].sort();
    if (DOM.gotraFilterSelect) {
      DOM.gotraFilterSelect.innerHTML = '<option value="all">All Gotras & Lineages</option>' +
        gotras.map(g => `<option value="${g}">${g}</option>`).join('');
    }

    // Standard Regions
    const regions = [
      'Gandaki',
      'Bagmati',
      'Koshi',
      'Lumbini',
      'Karnali',
      'Sudurpashchim',
      'Madhesh'
    ];
    if (DOM.regionFilterSelect) {
      DOM.regionFilterSelect.innerHTML = '<option value="all">All Regions</option>' +
        regions.map(r => `<option value="${r}">${r}</option>`).join('');
    }
  }

  /**
   * Render Category Filter Bar with counts
   */
  function renderCategoryFilterBar() {
    if (!DOM.categoryFilterBar || !window.CASTE_DATABASE) return;

    const categories = ['all', 'Khas-Arya', 'Newar', 'Indigenous Janajati', 'Madhesi / Terai', 'Dalit', 'Muslim'];

    const counts = { all: CASTE_DATABASE.length };
    CASTE_DATABASE.forEach(item => {
      counts[item.category] = (counts[item.category] || 0) + 1;
    });

    DOM.categoryFilterBar.innerHTML = categories.map(cat => {
      const label = cat === 'all' ? 'All Surnames' : cat;
      const count = counts[cat] || 0;
      const isActive = state.selectedCategory === cat ? 'active' : '';
      return `<button class="cat-pill ${isActive}" data-category="${cat}">
        <span>${label}</span>
        <span class="pill-count">${count}</span>
      </button>`;
    }).join('');
  }

  /**
   * Filter & Sort Logic
   */
  function getFilteredData() {
    if (!window.CASTE_DATABASE) return [];

    let filtered = CASTE_DATABASE.filter(item => {
      // Category filter
      if (state.selectedCategory !== 'all' && item.category !== state.selectedCategory) {
        return false;
      }

      // Community filter
      if (state.selectedCommunity !== 'all' && item.community !== state.selectedCommunity) {
        return false;
      }

      // Gotra filter
      if (state.selectedGotra !== 'all' && item.gotra !== state.selectedGotra) {
        return false;
      }

      // Region filter
      if (state.selectedRegion !== 'all' && !item.region.toLowerCase().includes(state.selectedRegion.toLowerCase())) {
        return false;
      }

      // Search Query filter (English & Devanagari fuzzy matching)
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase().trim();
        const searchCorpus = [
          item.surname,
          item.devanagari,
          item.community,
          item.subcaste_or_clan,
          item.gotra,
          item.gotra_devanagari,
          item.kuldevata,
          item.region,
          item.notes
        ].join(' ').toLowerCase();

        if (!searchCorpus.includes(q)) {
          return false;
        }
      }

      return true;
    });

    // Sorting
    filtered.sort((a, b) => {
      switch (state.sortBy) {
        case 'surname-asc':
          return a.surname.localeCompare(b.surname);
        case 'surname-desc':
          return b.surname.localeCompare(a.surname);
        case 'deva-asc':
          return a.devanagari.localeCompare(b.devanagari, 'ne');
        case 'category':
          return a.category.localeCompare(b.category) || a.surname.localeCompare(b.surname);
        case 'community':
          return a.community.localeCompare(b.community) || a.surname.localeCompare(b.surname);
        default:
          return a.id - b.id;
      }
    });

    return filtered;
  }

  /**
   * Main View Render Dispatcher
   */
  function render() {
    const data = getFilteredData();

    // Update Result count label
    if (DOM.resultsCount) {
      DOM.resultsCount.innerHTML = `Showing <strong>${data.length}</strong> verified surnames (नतिजा: <strong>${data.length}</strong>)`;
    }

    // Toggle Clear Search Button
    if (DOM.searchClearBtn) {
      DOM.searchClearBtn.style.display = state.searchQuery ? 'block' : 'none';
    }

    // Handle Views
    switch (state.viewMode) {
      case 'table':
        renderTableView(data);
        break;
      case 'sagotra':
        renderSagotraView();
        break;
      case 'checker':
        renderSagotraChecker();
        break;
      case 'insights':
        renderInsightsView();
        break;
      case 'grid':
      default:
        renderCardsView(data);
        break;
    }
  }

  /**
   * Render Cards Grid View
   */
  function renderCardsView(data) {
    if (!DOM.contentSection) return;

    if (data.length === 0) {
      renderEmptyState();
      if (DOM.paginationContainer) DOM.paginationContainer.style.display = 'none';
      return;
    }

    const itemsToShow = data.slice(0, state.page * state.pageSize);
    const hasMore = itemsToShow.length < data.length;

    const cardsHtml = `
      <div class="surnames-grid">
        ${itemsToShow.map(item => createCardHtml(item)).join('')}
      </div>
    `;

    DOM.contentSection.innerHTML = cardsHtml;

    // Pagination
    if (DOM.paginationContainer) {
      DOM.paginationContainer.style.display = hasMore ? 'flex' : 'none';
      if (DOM.loadMoreBtn) {
        DOM.loadMoreBtn.textContent = `Load More Surnames (${itemsToShow.length} of ${data.length})`;
      }
    }
  }

  /**
   * Create Individual Card HTML
   */
  function createCardHtml(item) {
    const isFav = state.favorites.has(item.id);
    const catConfig = CATEGORY_CONFIG[item.category] || { class: 'badge-khas', color: '#f59e0b' };

    return `
      <div class="surname-card" data-id="${item.id}">
        <div>
          <div class="card-top">
            <div class="card-title-group">
              <span class="card-devanagari">${escapeHtml(item.devanagari)}</span>
              <span class="card-roman">${escapeHtml(item.surname)}</span>
            </div>
            <button class="card-favorite-btn ${isFav ? 'favorited' : ''}" data-fav-id="${item.id}" title="${isFav ? 'Remove from saved' : 'Save surname'}" aria-label="Toggle Save">
              ${getFavIconSvg(isFav)}
            </button>
          </div>

          <div class="card-tags">
            <span class="badge ${catConfig.class}">
              <span class="badge-dot" style="background: ${catConfig.color};"></span>
              ${escapeHtml(item.category)}
            </span>
            <span class="badge">${escapeHtml(item.community)}</span>
          </div>

          <div class="card-meta-list">
            <div class="meta-row">
              <span class="meta-label">Gotra / Clan:</span>
              <span class="meta-value">${escapeHtml(item.gotra)}${item.gotra_devanagari ? ` (${item.gotra_devanagari})` : ''}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Kuldevata:</span>
              <span class="meta-value">${escapeHtml(item.kuldevata)}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Region:</span>
              <span class="meta-value">${escapeHtml(item.region)}</span>
            </div>
          </div>
        </div>

        <div class="card-footer">
          <button class="card-view-btn" data-view-id="${item.id}">
            <span>View Details</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </button>
          <span style="font-size: 0.75rem; color: var(--text-muted); font-family: monospace;">#${item.id}</span>
        </div>
      </div>
    `;
  }

  /**
   * Render Responsive Table View
   */
  function renderTableView(data) {
    if (!DOM.contentSection) return;

    if (data.length === 0) {
      renderEmptyState();
      if (DOM.paginationContainer) DOM.paginationContainer.style.display = 'none';
      return;
    }

    const itemsToShow = data.slice(0, state.page * state.pageSize);
    const hasMore = itemsToShow.length < data.length;

    const tableHtml = `
      <div class="table-container">
        <table class="responsive-table">
          <thead>
            <tr>
              <th data-sort="surname-asc">Surname</th>
              <th data-sort="category">Category</th>
              <th data-sort="community">Community</th>
              <th>Gotra / Clan</th>
              <th>Kuldevata</th>
              <th>Primary Region</th>
              <th style="text-align: center; width: 60px;">Saved</th>
            </tr>
          </thead>
          <tbody>
            ${itemsToShow.map(item => {
              const isFav = state.favorites.has(item.id);
              const catConfig = CATEGORY_CONFIG[item.category] || { class: 'badge-khas', color: '#f59e0b' };
              return `
                <tr data-id="${item.id}">
                  <td>
                    <div class="table-surname-cell">
                      <span class="table-surname-dev">${escapeHtml(item.devanagari)}</span>
                      <span class="table-surname-rom">${escapeHtml(item.surname)}</span>
                    </div>
                  </td>
                  <td>
                    <span class="badge ${catConfig.class}">
                      <span class="badge-dot" style="background: ${catConfig.color};"></span>
                      ${escapeHtml(item.category)}
                    </span>
                  </td>
                  <td><strong>${escapeHtml(item.community)}</strong></td>
                  <td>${escapeHtml(item.gotra)}${item.gotra_devanagari ? ` (${item.gotra_devanagari})` : ''}</td>
                  <td>${escapeHtml(item.kuldevata)}</td>
                  <td>${escapeHtml(item.region)}</td>
                  <td style="text-align: center;" onclick="event.stopPropagation();">
                    <button class="btn btn-icon" data-fav-id="${item.id}" title="Toggle Save" style="width: 28px; height: 28px;">
                      ${getFavIconSvg(isFav)}
                    </button>
                  </td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      </div>
    `;

    DOM.contentSection.innerHTML = tableHtml;

    // Pagination
    if (DOM.paginationContainer) {
      DOM.paginationContainer.style.display = hasMore ? 'flex' : 'none';
      if (DOM.loadMoreBtn) {
        DOM.loadMoreBtn.textContent = `Load More Surnames (${itemsToShow.length} of ${data.length})`;
      }
    }
  }

  /**
   * Render Sagotra / Gotra Bandhav Lineage Finder View
   */
  function renderSagotraView() {
    if (!DOM.contentSection || !window.CASTE_DATABASE) return;
    if (DOM.paginationContainer) DOM.paginationContainer.style.display = 'none';

    // Group surnames by gotra
    const gotraGroups = {};
    CASTE_DATABASE.forEach(item => {
      const g = item.gotra;
      if (!gotraGroups[g]) {
        gotraGroups[g] = [];
      }
      gotraGroups[g].push(item);
    });

    const sortedGotras = Object.keys(gotraGroups).sort();
    const activeGotra = state.selectedGotra !== 'all' ? state.selectedGotra : sortedGotras[0];
    const relatedList = gotraGroups[activeGotra] || [];
    const sampleRecord = relatedList[0] || {};

    const gotraExplorerItems = sortedGotras.map(g => {
      const sample = gotraGroups[g][0];
      const deva = sample && sample.gotra_devanagari ? sample.gotra_devanagari : g;
      return {
        id: g,
        titleDev: deva,
        titleRom: g,
        badge: `${gotraGroups[g].length} surnames`,
        gotra: '',
        searchCorpus: `${g} ${deva}`.toLowerCase()
      };
    });

    const currentGotraObj = gotraExplorerItems.find(x => x.id === activeGotra) || gotraExplorerItems[0];

    const sagotraHtml = `
      <div class="sagotra-finder-container">
        <div class="sagotra-header">
          <h2>Gotra Lineage Explorer</h2>
          <p>Choose your Gotra or clan lineage to discover all Nepali surnames that share the same Gotra and traditional ancestry (सगोत्रीय बन्धुहरू).</p>
        </div>

        <div class="gotra-picker-wrapper" style="max-width: 480px; margin: 0 auto 1.75rem;">
          <label class="gotra-picker-label" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: var(--text-secondary);">Search or Select Gotra / Lineage:</label>
          ${renderComboboxHtml({
            id: 'sagotraCombobox',
            selectedDev: currentGotraObj ? currentGotraObj.titleDev : '',
            selectedRom: currentGotraObj ? currentGotraObj.titleRom : activeGotra,
            selectedMeta: `• ${relatedList.length} surnames`,
            placeholder: 'Type gotra name (e.g. Kaudinya, Kashyap, Bharadwaj)...'
          })}
        </div>

        <div class="sagotra-results-box">
          <div class="sagotra-info-banner">
            <div>
              <span class="meta-label">Selected Lineage:</span>
              <h3 style="color: var(--brand-primary); font-size: 1.4rem;">${escapeHtml(activeGotra)}</h3>
            </div>
            <div>
              <span class="meta-label">Pravara / Lineage:</span>
              <p style="font-weight: 600; color: var(--text-primary);">${escapeHtml(sampleRecord.pravara || 'Traditional Clan Lineage')}</p>
            </div>
            <div>
              <span class="meta-label">Common Kuldevata:</span>
              <p style="font-weight: 600; color: var(--text-primary);">${escapeHtml(sampleRecord.kuldevata || 'Ancestral Deity')}</p>
            </div>
            <div>
              <span class="meta-label">Total Sister Surnames:</span>
              <p style="font-weight: 800; font-size: 1.25rem; color: var(--brand-primary);">${relatedList.length}</p>
            </div>
          </div>

          <h4 style="margin-bottom: 1rem; color: var(--text-primary);">Surnames Sharing This Gotra / Lineage:</h4>
          <div class="sagotra-surnames-cloud">
            ${relatedList.map(item => `
              <div class="sagotra-chip" data-id="${item.id}">
                <span class="chip-dev">${escapeHtml(item.devanagari)}</span>
                <span class="chip-rom">(${escapeHtml(item.surname)})</span>
                <span class="chip-comm">• ${escapeHtml(item.community)}</span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;

    DOM.contentSection.innerHTML = sagotraHtml;

    // Attach searchable combobox to sagotra selector
    setupCombobox({
      containerId: 'sagotraCombobox',
      items: gotraExplorerItems,
      selectedId: activeGotra,
      onSelect: (selectedGotra) => {
        state.selectedGotra = selectedGotra;
        if (DOM.gotraFilterSelect) DOM.gotraFilterSelect.value = selectedGotra;
        renderSagotraView();
      }
    });
  }

  /**
   * Evaluate Couple Gotra Compatibility
   */
  function evaluateCompatibility(partnerA, partnerB, mamaA, mamaB) {
    if (!partnerA || !partnerB) return null;

    const gotraA = (checkerState.partnerAGotra || partnerA.gotra || '').trim();
    const gotraB = (checkerState.partnerBGotra || partnerB.gotra || '').trim();

    const normA = gotraA.toLowerCase();
    const normB = gotraB.toLowerCase();

    const isVedicA = !normA.includes('clan') && !normA.includes('guthi') && !normA.includes('islamic') && !normA.includes('not applicable');
    const isVedicB = !normB.includes('clan') && !normB.includes('guthi') && !normB.includes('islamic') && !normB.includes('not applicable');

    let isDirectCollision = false;
    if (normA && normB && (normA === normB || normA.includes(normB) || normB.includes(normA))) {
      if (!normA.includes('clan lineage') && !normA.includes('not applicable')) {
        isDirectCollision = true;
      }
    }

    // Maternal Gotra Check
    let isMamaCollision = false;
    let mamaCollisionDetails = '';
    if (mamaA && normB && (mamaA.toLowerCase() === normB || normB.includes(mamaA.toLowerCase()))) {
      isMamaCollision = true;
      mamaCollisionDetails = `Partner 1's Maternal Gotra (${mamaA}) matches Partner 2's Gotra (${gotraB})`;
    } else if (mamaB && normA && (mamaB.toLowerCase() === normA || normA.includes(mamaB.toLowerCase()))) {
      isMamaCollision = true;
      mamaCollisionDetails = `Partner 2's Maternal Gotra (${mamaB}) matches Partner 1's Gotra (${gotraA})`;
    }

    // Janajati Clan Check
    let isJanajatiSameClan = false;
    if (partnerA.category === 'Indigenous Janajati' && partnerB.category === 'Indigenous Janajati') {
      if (partnerA.community === partnerB.community) {
        const subA = (partnerA.subcaste_or_clan || partnerA.surname).toLowerCase().trim();
        const subB = (partnerB.subcaste_or_clan || partnerB.surname).toLowerCase().trim();
        if (subA && subB && (subA === subB || partnerA.surname.toLowerCase() === partnerB.surname.toLowerCase())) {
          isJanajatiSameClan = true;
        }
      }
    }

    // Pravara Overlap Check
    let isPravaraOverlap = false;
    if (partnerA.pravara && partnerB.pravara && isVedicA && isVedicB && !isDirectCollision) {
      const rishisA = new Set(partnerA.pravara.toLowerCase().match(/[a-z]{4,}/g) || []);
      const rishisB = new Set(partnerB.pravara.toLowerCase().match(/[a-z]{4,}/g) || []);
      ['tryarshi', 'pancharshi', 'ekarshi', 'lineage'].forEach(w => { rishisA.delete(w); rishisB.delete(w); });
      const intersection = [...rishisA].filter(r => rishisB.has(r));
      if (intersection.length >= 2) {
        isPravaraOverlap = true;
      }
    }

    // Verdict Formulation
    if (isDirectCollision || isJanajatiSameClan) {
      return {
        status: 'collision',
        icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`,
        titleNepali: 'सगोत्र / स्वथर मिलान (Gotra Collision Detected)',
        titleEnglish: 'Direct Gotra / Clan Collision Detected',
        subtitle: `${partnerA.surname} (${gotraA}) & ${partnerB.surname} (${gotraB})`,
        summary: `दुवै पक्षको गोत्र वा कुल एउटै (${gotraA}) परेको देखिन्छ। हिन्दू तथा खस–आर्य परम्परामा एउटै गोत्र भएकाहरूलाई ऋषि-परम्पराका आध्यात्मिक दाजु-बहिनी (सगोत्रीय बन्धु) मानिने हुनाले सगोत्र विवाह वर्जित मानिन्छ।`,
        geneticNote: `वैज्ञानिक तथा चिकित्सा दृष्टिकोणबाट पनि नजिकको वंशाणुगत नाता (Consanguinity) मा विवाह गर्दा सन्तानमा सुप्त वंशाणुगत रोगहरू (Autosomal Recessive Disorders) देखिने जोखिम बढी हुने हुनाले गोत्र भिन्नतालाई प्राथमिकता दिइन्छ।`,
        legalNote: `नेपालको प्रचलित मुलुकी देवानी संहिता, २०७४ बमोजिम कानुनले बालिग नागरिकलाई विवाहको स्वतन्त्रता दिएको भए तापनि परम्परागत हाडनाता करणी ऐन र सांस्कृतिक मान्यता अनुसार सगोत्र विवाह वर्जित रहँदै आएको छ।`
      };
    } else if (isMamaCollision) {
      return {
        status: 'warning',
        icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#eab308" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`,
        titleNepali: 'मावली गोत्र मिलान (Maternal Gotra Notice)',
        titleEnglish: 'Maternal Uncle (Mama) Gotra Overlap',
        subtitle: mamaCollisionDetails,
        summary: `एक पक्षको पितृ गोत्र अर्को पक्षको मावली गोत्र (आमाको माइतीको गोत्र) सँग मिलेको देखिन्छ। नेपाली समाजका कतिपय समुदायहरूमा ३ देखि ७ पुस्तासम्म मावली गोत्र छलेर मात्र विवाह गर्ने परम्परा छ।`,
        geneticNote: `मावली तर्फको वंशाणुगत निकटता कति पुस्तासम्म छ भनी पारिवारिक वंशावली हेरी थप निश्चित गर्न सल्लाह दिइन्छ।`,
        legalNote: `गोत्र भिन्न भए पनि मावली हाडनाता नपर्ने खण्डमा आपसी सहमतिमा विवाह मान्य हुन सक्छ।`
      };
    } else if (isPravaraOverlap) {
      return {
        status: 'warning',
        icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#eab308" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`,
        titleNepali: 'समान प्रवर सूचना (Shared Pravara Seers)',
        titleEnglish: 'Shared Pravara Lineage Notice',
        subtitle: `Gotras are distinct (${gotraA} vs ${gotraB}), but share common Pravara Rishis.`,
        summary: `गोत्रको नाम फरक भए तापनि प्रवर ऋषिहरूमा आंशिक समानता देखिन्छ। धर्मशास्त्रका कतिपय ग्रन्थहरूमा समान प्रवर भएका गोत्रबीच पनि विवाह विचारणीय मानिएको छ, यद्यपि आधुनिक समाजमा गोत्र फरक भएमा विवाह स्वीकार्य मानिन्छ।`,
        geneticNote: `धेरै प्राचीन ऋषि पुस्ताको समानता भए पनि निकट रक्तसम्बन्ध नभएमा वंशाणुगत जोखिम न्यून रहन्छ।`,
        legalNote: `गोत्र भिन्न रहेकाले कानुनी तथा सामाजिक रूपमा सामान्यतया कुनै बाधा रहँदैन।`
      };
    } else {
      return {
        status: 'clean',
        icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`,
        titleNepali: 'भिन्न गोत्र - विवाहका लागि शुभ (No Gotra Collision)',
        titleEnglish: 'Distinct Gotras - Compatible',
        subtitle: `${partnerA.surname} (${gotraA}) & ${partnerB.surname} (${gotraB})`,
        summary: `दुवै पक्षको गोत्र भिन्न-भिन्न (${gotraA} र ${gotraB}) रहेकाले परम्परागत धर्मशास्त्र, वंशावली तथा गोत्र मान्यता अनुसार कुनै पनि सगोत्र टकराव (Collision) देखिँदैन। विवाहका लागि यो सम्बन्ध शास्त्रसम्मत मानिन्छ।`,
        geneticNote: `भिन्न गोत्र हुनुले दुई भिन्न वंश रेखाको मिलन जनाउँछ, जसले निकट रक्त-सम्बन्धबाट हुने वंशाणुगत रोगहरूको सम्भावनालाई न्यूनतम बनाउँछ।`,
        legalNote: `नेपालको प्रचलित कानुन र सामाजिक परम्परा दुवै अनुसार यो विवाह पूर्णतः मान्य छ।`
      };
    }
  }

  /**
   * Searchable Combobox Component Helpers
   */
  function renderComboboxHtml({ id, selectedDev, selectedRom, selectedMeta, placeholder }) {
    return `
      <div class="searchable-combobox" id="${id}">
        <div class="combobox-trigger" tabindex="0" role="combobox" aria-expanded="false" aria-label="${escapeHtml(placeholder)}">
          <div class="combobox-selected-info">
            <span class="combobox-selected-deva">${escapeHtml(selectedDev || '')}</span>
            <span class="combobox-selected-roman">${escapeHtml(selectedRom || '')}</span>
            <span class="combobox-selected-meta">${escapeHtml(selectedMeta || '')}</span>
          </div>
          <span class="combobox-chevron">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </span>
        </div>
        <div class="combobox-dropdown" style="display: none;">
          <div class="combobox-search-box">
            <svg class="combobox-search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" class="combobox-search-input" placeholder="${escapeHtml(placeholder)}" autocomplete="off" />
            <button class="combobox-clear-btn" style="display: none;" title="Clear">✕</button>
          </div>
          <div class="combobox-options-list" role="listbox"></div>
          <div class="combobox-footer">
            <span>Type to filter instantly</span>
            <span class="combobox-count"></span>
          </div>
        </div>
      </div>
    `;
  }

  function setupCombobox({ containerId, items, selectedId, onSelect }) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const trigger = container.querySelector('.combobox-trigger');
    const dropdown = container.querySelector('.combobox-dropdown');
    const searchInput = container.querySelector('.combobox-search-input');
    const clearBtn = container.querySelector('.combobox-clear-btn');
    const list = container.querySelector('.combobox-options-list');
    const countEl = container.querySelector('.combobox-count');

    let isOpen = false;

    function renderOptions(query = '') {
      const q = query.toLowerCase().trim();
      let matched = items;
      if (q) {
        matched = items.filter(it => it.searchCorpus.includes(q));
      }

      if (countEl) {
        countEl.textContent = `${matched.length} record${matched.length === 1 ? '' : 's'}`;
      }

      if (matched.length === 0) {
        list.innerHTML = `<div class="combobox-no-results">No records found matching "<strong>${escapeHtml(query)}</strong>"</div>`;
        return;
      }

      const toShow = matched.slice(0, 45);
      list.innerHTML = toShow.map(it => {
        const isSel = it.id === selectedId;
        return `
          <div class="combobox-option ${isSel ? 'selected' : ''}" data-item-id="${it.id}">
            <div class="combobox-option-title">
              <span class="combobox-option-deva">${escapeHtml(it.titleDev || '')}</span>
              <span class="combobox-option-roman">${escapeHtml(it.titleRom || '')}</span>
            </div>
            <div class="combobox-option-badges">
              ${it.badge ? `<span class="badge" style="font-size: 0.68rem; padding: 0.1rem 0.35rem;">${escapeHtml(it.badge)}</span>` : ''}
              ${it.gotra ? `<span style="color: var(--accent-gold); font-weight: 500;">${escapeHtml(it.gotra)}</span>` : ''}
            </div>
          </div>
        `;
      }).join('');
    }

    function openDropdown() {
      document.querySelectorAll('.combobox-dropdown').forEach(d => {
        if (d !== dropdown) d.style.display = 'none';
      });
      document.querySelectorAll('.combobox-trigger').forEach(t => {
        if (t !== trigger) t.classList.remove('active');
      });

      dropdown.style.display = 'flex';
      trigger.classList.add('active');
      isOpen = true;
      searchInput.value = '';
      if (clearBtn) clearBtn.style.display = 'none';
      renderOptions('');
      setTimeout(() => searchInput.focus(), 50);
    }

    function closeDropdown() {
      dropdown.style.display = 'none';
      trigger.classList.remove('active');
      isOpen = false;
    }

    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      if (isOpen) {
        closeDropdown();
      } else {
        openDropdown();
      }
    });

    trigger.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') {
        e.preventDefault();
        openDropdown();
      }
    });

    searchInput.addEventListener('input', (e) => {
      const q = e.target.value;
      if (clearBtn) clearBtn.style.display = q ? 'block' : 'none';
      renderOptions(q);
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        searchInput.value = '';
        clearBtn.style.display = 'none';
        renderOptions('');
        searchInput.focus();
      });
    }

    list.addEventListener('click', (e) => {
      const opt = e.target.closest('.combobox-option');
      if (opt) {
        const rawId = opt.getAttribute('data-item-id');
        const finalId = (!isNaN(rawId) && rawId !== '') ? parseInt(rawId, 10) : rawId;
        closeDropdown();
        onSelect(finalId);
      }
    });

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeDropdown();
        trigger.focus();
      } else if (e.key === 'Enter') {
        const firstOpt = list.querySelector('.combobox-option');
        if (firstOpt) {
          const rawId = firstOpt.getAttribute('data-item-id');
          const finalId = (!isNaN(rawId) && rawId !== '') ? parseInt(rawId, 10) : rawId;
          closeDropdown();
          onSelect(finalId);
        }
      }
    });

    document.addEventListener('click', (e) => {
      if (!container.contains(e.target)) {
        closeDropdown();
      }
    });
  }

  /**
   * Render Couple Gotra & Sagotra Collision Checker View
   */
  function renderSagotraChecker() {
    if (!DOM.contentSection || !window.CASTE_DATABASE) return;
    if (DOM.paginationContainer) DOM.paginationContainer.style.display = 'none';

    if (!checkerState.partnerAId) checkerState.partnerAId = 1; // Acharya
    if (!checkerState.partnerBId) checkerState.partnerBId = 575; // Sapkota

    const partnerA = CASTE_DATABASE.find(x => x.id === checkerState.partnerAId) || CASTE_DATABASE[0];
    const partnerB = CASTE_DATABASE.find(x => x.id === checkerState.partnerBId) || CASTE_DATABASE[1];

    if (!checkerState.partnerAGotra) checkerState.partnerAGotra = partnerA.gotra;
    if (!checkerState.partnerBGotra) checkerState.partnerBGotra = partnerB.gotra;

    const evaluation = evaluateCompatibility(partnerA, partnerB, checkerState.partnerAMamaGotra, checkerState.partnerBMamaGotra);
    const uniqueGotras = [...new Set(CASTE_DATABASE.map(x => x.gotra).filter(g => g && !g.includes('Not Applicable')))].sort();

    // Prepare combobox items
    const surnameComboboxItems = CASTE_DATABASE.map(item => ({
      id: item.id,
      titleDev: item.devanagari,
      titleRom: item.surname,
      badge: item.community,
      gotra: item.gotra,
      searchCorpus: `${item.surname} ${item.devanagari} ${item.community} ${item.category} ${item.gotra} ${item.gotra_devanagari || ''}`.toLowerCase()
    }));

    const gotraComboboxItems = [
      { id: '', titleDev: 'मावली गोत्र उल्लेख नभएको', titleRom: 'No Maternal Gotra', badge: '', gotra: '', searchCorpus: 'no none not specified chaina' },
      ...uniqueGotras.map(g => {
        const sample = CASTE_DATABASE.find(x => x.gotra === g);
        const deva = sample && sample.gotra_devanagari ? sample.gotra_devanagari : g;
        return {
          id: g,
          titleDev: deva,
          titleRom: g,
          badge: 'Gotra',
          gotra: '',
          searchCorpus: `${g} ${deva}`.toLowerCase()
        };
      })
    ];

    const mamaAGotraObj = gotraComboboxItems.find(x => x.id === checkerState.partnerAMamaGotra) || gotraComboboxItems[0];
    const mamaBGotraObj = gotraComboboxItems.find(x => x.id === checkerState.partnerBMamaGotra) || gotraComboboxItems[0];

    const html = `
      <div class="couple-checker-container">
        <div class="checker-hero-header">
          <h2>Gotra Compatibility Checker</h2>
          <p>
            Verify whether prospective bride and groom share the same Gotra (सगोत्र), maternal lineage (मावली गोत्र), Pravara overlap, or clan exogamy under traditional Nepali cultural and genealogical guidelines.
          </p>
        </div>

        <!-- Couple Selection Row -->
        <div class="couple-selection-row">
          <!-- Partner A: Groom -->
          <div class="partner-card-select partner-card-groom">
            <div class="partner-card-head">
              <div class="partner-avatar avatar-groom">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              </div>
              <div class="partner-title-text">
                <span class="partner-role-nepali">Groom (वर पक्ष)</span>
                <span class="partner-role-eng">Patrilineal Lineage</span>
              </div>
            </div>

            <div class="partner-form-group">
              <label>Select Groom's Surname (वरको थर):</label>
              ${renderComboboxHtml({
                id: 'partnerACombobox',
                selectedDev: partnerA.devanagari,
                selectedRom: partnerA.surname,
                selectedMeta: `• ${partnerA.community}`,
                placeholder: 'Type surname or Devanagari (e.g. Acharya, सापकोटा)...'
              })}
            </div>

            <div class="partner-selected-box">
              <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <span style="font-family: var(--font-deva); font-size: 1.45rem; font-weight: 700; color: var(--text-primary);">${escapeHtml(partnerA.devanagari)}</span>
                <span style="font-size: 1.05rem; font-weight: 600; color: var(--accent-blue);">${escapeHtml(partnerA.surname)}</span>
              </div>
              <div style="font-size: 0.84rem; color: var(--text-secondary); margin-top: 0.25rem;">
                ${escapeHtml(partnerA.community)} • ${escapeHtml(partnerA.category)}
              </div>
              <div class="partner-gotra-badge" style="background: var(--accent-blue-soft); color: var(--accent-blue); border-color: rgba(37,99,235,0.25);">
                <span>Gotra:</span>
                <strong>${escapeHtml(partnerA.gotra)}${partnerA.gotra_devanagari ? ` (${partnerA.gotra_devanagari})` : ''}</strong>
              </div>
            </div>

            <div class="partner-form-group" style="margin-top: 1.15rem;">
              <label>Maternal Gotra (मावली गोत्र) - Optional:</label>
              ${renderComboboxHtml({
                id: 'partnerAMamaCombobox',
                selectedDev: mamaAGotraObj.titleDev,
                selectedRom: mamaAGotraObj.titleRom,
                selectedMeta: '',
                placeholder: 'Type to search Maternal Gotra (e.g. Kaudinya, Kashyap)...'
              })}
            </div>
          </div>

          <!-- Swap Button Center -->
          <div class="swap-btn-container">
            <button class="swap-partners-btn" id="swapPartnersBtn" title="Swap Bride & Groom" aria-label="Swap Bride and Groom">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path></svg>
            </button>
          </div>

          <!-- Partner B: Bride -->
          <div class="partner-card-select partner-card-bride">
            <div class="partner-card-head">
              <div class="partner-avatar avatar-bride">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
              </div>
              <div class="partner-title-text">
                <span class="partner-role-nepali">Bride (वधु पक्ष)</span>
                <span class="partner-role-eng">Patrilineal Lineage</span>
              </div>
            </div>

            <div class="partner-form-group">
              <label>Select Bride's Surname (वधुको थर):</label>
              ${renderComboboxHtml({
                id: 'partnerBCombobox',
                selectedDev: partnerB.devanagari,
                selectedRom: partnerB.surname,
                selectedMeta: `• ${partnerB.community}`,
                placeholder: 'Type surname or Devanagari (e.g. Sapkota, भट्टराई)...'
              })}
            </div>

            <div class="partner-selected-box">
              <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <span style="font-family: var(--font-deva); font-size: 1.45rem; font-weight: 700; color: var(--text-primary);">${escapeHtml(partnerB.devanagari)}</span>
                <span style="font-size: 1.05rem; font-weight: 600; color: var(--accent-rose);">${escapeHtml(partnerB.surname)}</span>
              </div>
              <div style="font-size: 0.84rem; color: var(--text-secondary); margin-top: 0.25rem;">
                ${escapeHtml(partnerB.community)} • ${escapeHtml(partnerB.category)}
              </div>
              <div class="partner-gotra-badge" style="background: var(--accent-rose-soft); color: var(--accent-rose); border-color: rgba(225,29,72,0.25);">
                <span>Gotra:</span>
                <strong>${escapeHtml(partnerB.gotra)}${partnerB.gotra_devanagari ? ` (${partnerB.gotra_devanagari})` : ''}</strong>
              </div>
            </div>

            <div class="partner-form-group" style="margin-top: 1.15rem;">
              <label>Maternal Gotra (मावली गोत्र) - Optional:</label>
              ${renderComboboxHtml({
                id: 'partnerBMamaCombobox',
                selectedDev: mamaBGotraObj.titleDev,
                selectedRom: mamaBGotraObj.titleRom,
                selectedMeta: '',
                placeholder: 'Type to search Maternal Gotra (e.g. Kaudinya, Kashyap)...'
              })}
            </div>
          </div>
        </div>

        <!-- Quick Demo Presets -->
        <div class="checker-presets-container">
          <span class="presets-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
            <span>Quick Test Scenarios:</span>
          </span>
          <div class="presets-chips-wrap">
            <button type="button" class="preset-chip" data-preset="acharya-sapkota">
              <span class="preset-dot dot-collision"></span>
              <span>Acharya + Sapkota</span>
              <span class="preset-badge">Kaudinya Collision</span>
            </button>
            <button type="button" class="preset-chip" data-preset="dahal-lamsal">
              <span class="preset-dot dot-collision"></span>
              <span>Dahal + Lamsal</span>
              <span class="preset-badge">Vatsa Collision</span>
            </button>
            <button type="button" class="preset-chip" data-preset="dulal-dahal">
              <span class="preset-dot dot-compatible"></span>
              <span>Dulal + Dahal</span>
              <span class="preset-badge">Atreya + Vatsa Compatible</span>
            </button>
            <button type="button" class="preset-chip" data-preset="gautam-pokhrel">
              <span class="preset-dot dot-collision"></span>
              <span>Gautam + Pokharel</span>
              <span class="preset-badge">Atreya Collision</span>
            </button>
          </div>
        </div>

        <!-- Results Display Box -->
        ${evaluation ? `
          <div class="collision-result-wrapper">
            <div class="collision-result-card result-${evaluation.status}">
              <div class="result-card-header">
                <div class="result-status-icon">${evaluation.icon}</div>
                <div>
                  <div class="result-status-title">${escapeHtml(evaluation.titleNepali)}</div>
                  <div class="result-status-subtitle">${escapeHtml(evaluation.subtitle)}</div>
                </div>
              </div>

              <div class="result-explanation-text">
                <p><strong>Verdict:</strong> ${escapeHtml(evaluation.summary)}</p>
                <p style="margin-top: 0.75rem;"><strong>Genetics & Biological Context:</strong> ${escapeHtml(evaluation.geneticNote)}</p>
                <p style="margin-top: 0.75rem;"><strong>Legal & Social Context:</strong> ${escapeHtml(evaluation.legalNote)}</p>
              </div>

              <!-- Comparative Lineage Table -->
              <table class="lineage-compare-table">
                <thead>
                  <tr>
                    <th>Lineage Attribute</th>
                    <th>Groom: ${escapeHtml(partnerA.surname)}</th>
                    <th>Bride: ${escapeHtml(partnerB.surname)}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Devanagari Name</strong></td>
                    <td style="font-family: var(--font-deva); font-weight: 700;">${escapeHtml(partnerA.devanagari)}</td>
                    <td style="font-family: var(--font-deva); font-weight: 700;">${escapeHtml(partnerB.devanagari)}</td>
                  </tr>
                  <tr>
                    <td><strong>Community / Caste</strong></td>
                    <td>${escapeHtml(partnerA.community)} (${escapeHtml(partnerA.category)})</td>
                    <td>${escapeHtml(partnerB.community)} (${escapeHtml(partnerB.category)})</td>
                  </tr>
                  <tr>
                    <td><strong>Gotra</strong></td>
                    <td><strong style="color: var(--brand-text);">${escapeHtml(partnerA.gotra)}</strong></td>
                    <td><strong style="color: var(--brand-text);">${escapeHtml(partnerB.gotra)}</strong></td>
                  </tr>
                  <tr>
                    <td><strong>Pravara / Seers</strong></td>
                    <td>${escapeHtml(partnerA.pravara || 'Traditional Lineage')}</td>
                    <td>${escapeHtml(partnerB.pravara || 'Traditional Lineage')}</td>
                  </tr>
                  <tr>
                    <td><strong>Kuldevata</strong></td>
                    <td>${escapeHtml(partnerA.kuldevata)}</td>
                    <td>${escapeHtml(partnerB.kuldevata)}</td>
                  </tr>
                  <tr>
                    <td><strong>Homeland Region</strong></td>
                    <td>${escapeHtml(partnerA.region)}</td>
                    <td>${escapeHtml(partnerB.region)}</td>
                  </tr>
                </tbody>
              </table>

              <div class="result-footer-actions">
                <span style="font-size: 0.85rem; color: var(--text-secondary);">
                  Status: <strong>${evaluation.titleEnglish}</strong>
                </span>
                <div style="display: flex; gap: 0.6rem;">
                  <button class="btn btn-outline" id="copyReportBtn">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                    <span>Copy Report</span>
                  </button>
                  <button class="btn btn-primary" id="shareReportBtn">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
                    <span>Share Result</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ` : ''}
      </div>
    `;

    DOM.contentSection.innerHTML = html;

    // Initialize Searchable Comboboxes
    setupCombobox({
      containerId: 'partnerACombobox',
      items: surnameComboboxItems,
      selectedId: checkerState.partnerAId,
      onSelect: (selectedId) => {
        checkerState.partnerAId = selectedId;
        const item = CASTE_DATABASE.find(x => x.id === selectedId);
        if (item) checkerState.partnerAGotra = item.gotra;
        renderSagotraChecker();
      }
    });

    setupCombobox({
      containerId: 'partnerBCombobox',
      items: surnameComboboxItems,
      selectedId: checkerState.partnerBId,
      onSelect: (selectedId) => {
        checkerState.partnerBId = selectedId;
        const item = CASTE_DATABASE.find(x => x.id === selectedId);
        if (item) checkerState.partnerBGotra = item.gotra;
        renderSagotraChecker();
      }
    });

    setupCombobox({
      containerId: 'partnerAMamaCombobox',
      items: gotraComboboxItems,
      selectedId: checkerState.partnerAMamaGotra,
      onSelect: (selectedGotra) => {
        checkerState.partnerAMamaGotra = selectedGotra;
        renderSagotraChecker();
      }
    });

    setupCombobox({
      containerId: 'partnerBMamaCombobox',
      items: gotraComboboxItems,
      selectedId: checkerState.partnerBMamaGotra,
      onSelect: (selectedGotra) => {
        checkerState.partnerBMamaGotra = selectedGotra;
        renderSagotraChecker();
      }
    });

    // Swap button
    const swapBtn = document.getElementById('swapPartnersBtn');
    if (swapBtn) {
      swapBtn.addEventListener('click', () => {
        const tempId = checkerState.partnerAId;
        const tempGotra = checkerState.partnerAGotra;
        const tempMama = checkerState.partnerAMamaGotra;

        checkerState.partnerAId = checkerState.partnerBId;
        checkerState.partnerAGotra = checkerState.partnerBGotra;
        checkerState.partnerAMamaGotra = checkerState.partnerBMamaGotra;

        checkerState.partnerBId = tempId;
        checkerState.partnerBGotra = tempGotra;
        checkerState.partnerBMamaGotra = tempMama;

        renderSagotraChecker();
        showToast('Swapped Bride and Groom positions!');
      });
    }

    // Preset scenarios
    const presetBtns = DOM.contentSection.querySelectorAll('[data-preset]');
    presetBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const p = btn.getAttribute('data-preset');
        if (p === 'acharya-sapkota') {
          const a = CASTE_DATABASE.find(x => x.surname === 'Acharya');
          const b = CASTE_DATABASE.find(x => x.surname === 'Sapkota');
          if (a && b) {
            checkerState.partnerAId = a.id;
            checkerState.partnerAGotra = a.gotra;
            checkerState.partnerBId = b.id;
            checkerState.partnerBGotra = b.gotra;
          }
        } else if (p === 'dahal-lamsal') {
          const a = CASTE_DATABASE.find(x => x.surname === 'Dahal');
          const b = CASTE_DATABASE.find(x => x.surname === 'Lamsal');
          if (a && b) {
            checkerState.partnerAId = a.id;
            checkerState.partnerAGotra = a.gotra;
            checkerState.partnerBId = b.id;
            checkerState.partnerBGotra = b.gotra;
          }
        } else if (p === 'dulal-dahal') {
          const a = CASTE_DATABASE.find(x => x.surname === 'Dulal');
          const b = CASTE_DATABASE.find(x => x.surname === 'Dahal');
          if (a && b) {
            checkerState.partnerAId = a.id;
            checkerState.partnerAGotra = a.gotra;
            checkerState.partnerBId = b.id;
            checkerState.partnerBGotra = b.gotra;
          }
        } else if (p === 'gautam-pokhrel') {
          const a = CASTE_DATABASE.find(x => x.surname === 'Gautam');
          const b = CASTE_DATABASE.find(x => x.surname === 'Pokhrel/Pokharel');
          if (a && b) {
            checkerState.partnerAId = a.id;
            checkerState.partnerAGotra = a.gotra;
            checkerState.partnerBId = b.id;
            checkerState.partnerBGotra = b.gotra;
          }
        }
        renderSagotraChecker();
      });
    });

    const copyReportBtn = document.getElementById('copyReportBtn');
    const shareReportBtn = document.getElementById('shareReportBtn');

    if (copyReportBtn && evaluation) {
      copyReportBtn.addEventListener('click', () => {
        const text = `नेपाली सगोत्र विवाह जाँच प्रतिवेदन (Couple Gotra Compatibility Report):\n` +
          `वर (Groom): ${partnerA.surname} (${partnerA.devanagari}) - गोत्र: ${partnerA.gotra}\n` +
          `वधु (Bride): ${partnerB.surname} (${partnerB.devanagari}) - गोत्र: ${partnerB.gotra}\n` +
          `निस्कर्ष (Verdict): ${evaluation.titleNepali}\n` +
          `विवरण: ${evaluation.summary}\n` +
          `स्रोत: नेपालका जातजाति, थर तथा गोत्र संकलन पोर्टल`;
        navigator.clipboard.writeText(text).then(() => {
          showToast('Copied compatibility report to clipboard!');
        });
      });
    }

    if (shareReportBtn && evaluation) {
      shareReportBtn.addEventListener('click', () => {
        if (navigator.share) {
          navigator.share({
            title: `Couple Gotra Compatibility: ${partnerA.surname} & ${partnerB.surname}`,
            text: `Gotra check between ${partnerA.surname} (${partnerA.gotra}) and ${partnerB.surname} (${partnerB.gotra}): ${evaluation.titleNepali}`,
            url: window.location.href
          }).catch(() => {});
        } else {
          navigator.clipboard.writeText(window.location.href).then(() => {
            showToast('Link copied to clipboard!');
          });
        }
      });
    }
  }

  /**
   * Render Demographics & Cultural Insights View
   */
  function renderInsightsView() {
    if (!DOM.contentSection || !window.CASTE_DATABASE) return;
    if (DOM.paginationContainer) DOM.paginationContainer.style.display = 'none';

    // Compute distribution
    const catCounts = {};
    CASTE_DATABASE.forEach(item => {
      catCounts[item.category] = (catCounts[item.category] || 0) + 1;
    });

    const total = CASTE_DATABASE.length;

    const insightsHtml = `
      <div class="insights-container">
        <div class="insights-grid">
          <!-- Demographic Distribution -->
          <div class="insight-card">
            <h3>📊 Ethnic & Cultural Representation</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.25rem;">
              Breakdown of 700+ documented Nepali surnames across major historic and anthropological categories.
            </p>
            <div class="dist-bar-list">
              ${Object.entries(catCounts).map(([cat, count]) => {
                const pct = ((count / total) * 100).toFixed(1);
                const color = (CATEGORY_CONFIG[cat] && CATEGORY_CONFIG[cat].color) || '#f59e0b';
                return `
                  <div class="dist-bar-item">
                    <div class="dist-bar-label">
                      <span>${cat}</span>
                      <span><strong>${count}</strong> (${pct}%)</span>
                    </div>
                    <div class="dist-bar-track">
                      <div class="dist-bar-fill" style="width: ${pct}%; background-color: ${color};"></div>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Cultural Foundations -->
          <div class="insight-card">
            <h3>📜 Understanding Lineage Systems in Nepal</h3>
            <div class="guide-list">
              <div class="guide-item">
                <div class="guide-header">1. What is Gotra (गोत्र)? <span>+</span></div>
                <div class="guide-body">
                  In Khas-Arya and Vedic traditions, Gotra represents unbroken patrilineal descent from foundational Vedic seers (Saptarshi). It governs exogamous marriages (same gotra individuals consider themselves spiritual siblings).
                </div>
              </div>
              <div class="guide-item">
                <div class="guide-header">2. Newar Guthi & Guild Heritage <span>+</span></div>
                <div class="guide-body">
                  Newar society in Kathmandu Valley developed an extraordinary guild and Guthi (trust) system combining Hindu and Buddhist lineages, maintaining sacred dances, chariot festivals, artisan craftsmanship, and clan deity (Digu Dya) worship.
                </div>
              </div>
              <div class="guide-item">
                <div class="guide-header">3. Kirat Mundhum, Phaid & Janajati Clans <span>+</span></div>
                <div class="guide-body">
                  Indigenous communities such as Rai, Limbu, Magar, Tamang, and Gurung organize through clan structures (Phaid, Samet, Thar, Rhu). Governed by oral scriptures like the Kirat Mundhum, they venerate nature, hearth stones, and ancestral protectors.
                </div>
              </div>
              <div class="guide-item">
                <div class="guide-header">4. Constitutional Equality & Social Harmony <span>+</span></div>
                <div class="guide-body">
                  The modern Constitution of Nepal guarantees full equality, outlawing discrimination based on caste or origin (Articles 18 and 24). This portal serves educational and genealogical appreciation of Nepal's cultural diversity.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    DOM.contentSection.innerHTML = insightsHtml;

    // Collapsible accordion triggers
    const guideHeaders = DOM.contentSection.querySelectorAll('.guide-header');
    guideHeaders.forEach(h => {
      h.addEventListener('click', () => {
        const body = h.nextElementSibling;
        const isOpen = body.style.display === 'block';
        body.style.display = isOpen ? 'none' : 'block';
        h.querySelector('span').textContent = isOpen ? '+' : '−';
      });
    });
  }

  /**
   * Render Empty Search State
   */
  function renderEmptyState() {
    if (!DOM.contentSection) return;

    const hasActiveFilters = state.selectedCategory !== 'all' || 
                             state.selectedCommunity !== 'all' || 
                             state.selectedGotra !== 'all' || 
                             state.selectedRegion !== 'all';

    DOM.contentSection.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>No Surnames Found</h3>
        <p>No results matched your search "${escapeHtml(state.searchQuery)}"${hasActiveFilters ? ' with your current community/category filters applied' : ''}. Try searching in Devanagari (e.g., आचार्य, महर्जन), or clear your filter criteria.</p>
        <div style="display: flex; gap: 0.75rem; justify-content: center; margin-top: 1.25rem; flex-wrap: wrap;">
          ${hasActiveFilters ? `<button class="btn btn-outline" id="emptyClearFiltersBtn" style="border-color: var(--brand-primary); color: var(--brand-primary);">Clear Filters &amp; Keep Search</button>` : ''}
          <button class="btn btn-primary" id="emptyResetBtn">Reset All Filters &amp; Search</button>
        </div>
      </div>
    `;

    const emptyClearFiltersBtn = document.getElementById('emptyClearFiltersBtn');
    if (emptyClearFiltersBtn) {
      emptyClearFiltersBtn.addEventListener('click', () => {
        state.selectedCategory = 'all';
        state.selectedCommunity = 'all';
        state.selectedGotra = 'all';
        state.selectedRegion = 'all';
        if (DOM.communityFilterSelect) DOM.communityFilterSelect.value = 'all';
        if (DOM.gotraFilterSelect) DOM.gotraFilterSelect.value = 'all';
        if (DOM.regionFilterSelect) DOM.regionFilterSelect.value = 'all';
        renderCategoryFilterBar();
        render();
        showToast('Cleared category/community filters');
      });
    }

    const emptyResetBtn = document.getElementById('emptyResetBtn');
    if (emptyResetBtn) {
      emptyResetBtn.addEventListener('click', resetFilters);
    }
  }

  /**
   * Open Detail Modal
   */
  function openDetailModal(item) {
    state.activeSurname = item;
    const catConfig = CATEGORY_CONFIG[item.category] || { class: 'badge-khas', color: '#f59e0b' };
    const isFav = state.favorites.has(item.id);

    // Find Sagotra sister surnames
    const sagotraList = CASTE_DATABASE.filter(x => x.gotra === item.gotra && x.id !== item.id);

    const modalHtml = `
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title-box">
            <div style="display: flex; align-items: baseline; gap: 0.65rem; flex-wrap: wrap;">
              <span class="modal-title-dev">${escapeHtml(item.devanagari)}</span>
              <span class="modal-title-rom">${escapeHtml(item.surname)}</span>
            </div>
            <div style="margin-top: 0.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
              <span class="badge ${catConfig.class}">${escapeHtml(item.category)}</span>
              <span class="badge" style="background: var(--bg-surface-elevated); border: 1px solid var(--border-subtle); color: var(--text-secondary);">${escapeHtml(item.community)}</span>
            </div>
          </div>
          <button class="modal-close-btn" id="modalCloseBtnInner" title="Close">✕</button>
        </div>

        <div class="modal-body">
          <div class="detail-section">
            <span class="detail-section-title">🏛️ Lineage & Identity (वंश तथा पहिचान)</span>
            <div class="detail-grid">
              <div class="detail-box">
                <div class="detail-box-label">Caste / Community (जात/समुदाय):</div>
                <div class="detail-box-value">${escapeHtml(item.community)}</div>
              </div>
              <div class="detail-box">
                <div class="detail-box-label">Clan / Sub-caste / Thar (उपथर/शाखा):</div>
                <div class="detail-box-value">${escapeHtml(item.subcaste_or_clan || 'Primary Clan Lineage')}</div>
              </div>
              <div class="detail-box">
                <div class="detail-box-label">Gotra (गोत्र):</div>
                <div class="detail-box-value gold-highlight">${escapeHtml(item.gotra)}${item.gotra_devanagari ? ` (${item.gotra_devanagari})` : ''}</div>
              </div>
              <div class="detail-box">
                <div class="detail-box-label">Pravara / Rishis (प्रवर):</div>
                <div class="detail-box-value">${escapeHtml(item.pravara || 'Traditional Lineage')}</div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <span class="detail-section-title">🛕 Spiritual & Regional Roots (कुलदेवता तथा उद्गम)</span>
            <div class="detail-grid">
              <div class="detail-box">
                <div class="detail-box-label">Kuldevata (कुलदेवता):</div>
                <div class="detail-box-value gold-highlight">${escapeHtml(item.kuldevata)}</div>
              </div>
              <div class="detail-box">
                <div class="detail-box-label">Traditional Homeland / Concentration:</div>
                <div class="detail-box-value">${escapeHtml(item.region)}</div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <span class="detail-section-title">📜 Historical Significance & Cultural Context (इतिहास र महत्त्व)</span>
            <div class="notes-box">
              ${escapeHtml(item.notes)}
            </div>
          </div>

          ${sagotraList.length > 0 ? `
            <div class="detail-section">
              <span class="detail-section-title">🤝 Sagotra Surnames (${sagotraList.length} sister surnames sharing this Gotra):</span>
              <div class="sagotra-surnames-cloud">
                ${sagotraList.slice(0, 20).map(s => `
                  <button class="sagotra-chip" data-id="${s.id}">
                    <span class="chip-dev">${escapeHtml(s.devanagari)}</span>
                    <span class="chip-rom">(${escapeHtml(s.surname)})</span>
                  </button>
                `).join('')}
                ${sagotraList.length > 20 ? `<span style="font-size: 0.8rem; color: var(--text-muted); align-self: center;">+ ${sagotraList.length - 20} more</span>` : ''}
              </div>
            </div>
          ` : ''}
        </div>

        <div class="modal-footer">
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <button class="btn btn-outline" id="modalFavToggleBtn">
              ${isFav ? '❤️ Saved' : '🤍 Add to Favorites'}
            </button>
            <button class="btn btn-outline" id="modalCheckGotraBtn" style="border-color: var(--accent-gold); color: var(--accent-gold);">
              💍 Check Marriage Gotra
            </button>
          </div>
          <div style="display: flex; gap: 0.5rem;">
            <button class="btn btn-outline" id="modalCopyBtn">📋 Copy Details</button>
            <button class="btn btn-primary" id="modalShareBtn">🔗 Share</button>
          </div>
        </div>
      </div>
    `;

    DOM.modalOverlay.innerHTML = modalHtml;
    DOM.modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Modal Inner Events
    document.getElementById('modalCloseBtnInner').addEventListener('click', closeDetailModal);

    const checkGotraBtn = document.getElementById('modalCheckGotraBtn');
    if (checkGotraBtn) {
      checkGotraBtn.addEventListener('click', () => {
        checkerState.partnerAId = item.id;
        checkerState.partnerAGotra = item.gotra;
        checkerState.evaluated = true;
        state.viewMode = 'checker';
        closeDetailModal();
        const allTabs = [DOM.viewGridBtn, DOM.viewTableBtn, DOM.viewSagotraBtn, DOM.viewCheckerBtn, DOM.viewInsightsBtn];
        allTabs.forEach(b => b && b.classList.remove('active'));
        if (DOM.viewCheckerBtn) DOM.viewCheckerBtn.classList.add('active');
        render();
        showToast(`Pre-selected ${item.surname} (${item.devanagari}) in Couple Gotra Checker!`);
      });
    }

    const favToggleBtn = document.getElementById('modalFavToggleBtn');
    if (favToggleBtn) {
      favToggleBtn.addEventListener('click', () => {
        toggleFavorite(item.id);
        const nowFav = state.favorites.has(item.id);
        favToggleBtn.textContent = nowFav ? '❤️ Saved in Favorites' : '🤍 Add to Favorites';
      });
    }

    const copyBtn = document.getElementById('modalCopyBtn');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const text = `Nepali Surname: ${item.surname} (${item.devanagari})\nCaste/Community: ${item.community}\nCategory: ${item.category}\nGotra: ${item.gotra}\nKuldevata: ${item.kuldevata}\nRegion: ${item.region}\nNotes: ${item.notes}\nSource: Castes of Nepal Portal`;
        navigator.clipboard.writeText(text).then(() => {
          showToast('Copied full surname details to clipboard!');
        });
      });
    }

    const shareBtn = document.getElementById('modalShareBtn');
    if (shareBtn) {
      shareBtn.addEventListener('click', () => {
        if (navigator.share) {
          navigator.share({
            title: `${item.surname} (${item.devanagari}) - Nepali Caste & Gotra`,
            text: `Information on ${item.surname} (${item.devanagari}), Gotra: ${item.gotra}, Kuldevata: ${item.kuldevata}`,
            url: window.location.href
          }).catch(() => {});
        } else {
          navigator.clipboard.writeText(window.location.href).then(() => {
            showToast('Page link copied to clipboard!');
          });
        }
      });
    }

    // Sister chip click
    const sisterChips = DOM.modalOverlay.querySelectorAll('.sagotra-chip');
    sisterChips.forEach(chip => {
      chip.addEventListener('click', () => {
        const id = parseInt(chip.getAttribute('data-id'), 10);
        const sisterItem = CASTE_DATABASE.find(x => x.id === id);
        if (sisterItem) {
          openDetailModal(sisterItem);
        }
      });
    });
  }

  function closeDetailModal() {
    DOM.modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
    state.activeSurname = null;
  }

  /**
   * Bookmarks / Favorites Management
   */
  function toggleFavorite(id) {
    const numId = parseInt(id, 10);
    if (state.favorites.has(numId)) {
      state.favorites.delete(numId);
      showToast('Removed from favorites');
    } else {
      state.favorites.add(numId);
      showToast('Saved to favorites! ❤️');
    }

    localStorage.setItem('nepal_surnames_favs', JSON.stringify([...state.favorites]));
    updateFavBadge();
    renderFavoritesDrawer();

    // Update favorite icons on current view
    const favButtons = document.querySelectorAll(`[data-fav-id="${numId}"]`);
    favButtons.forEach(btn => {
      const isFav = state.favorites.has(numId);
      btn.classList.toggle('favorited', isFav);
      btn.textContent = isFav ? '❤️' : '🤍';
    });
  }

  function updateFavBadge() {
    if (DOM.favBadgeCount) {
      DOM.favBadgeCount.textContent = state.favorites.size;
    }
  }

  function openFavoritesDrawer() {
    renderFavoritesDrawer();
    DOM.drawerOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeFavoritesDrawer() {
    DOM.drawerOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  function renderFavoritesDrawer() {
    if (!DOM.drawerList || !window.CASTE_DATABASE) return;

    if (state.favorites.size === 0) {
      DOM.drawerList.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🤍</div>
          <h4>No Favorites Saved Yet</h4>
          <p style="font-size: 0.85rem; margin-top: 0.5rem;">Click the heart icon on any surname card or table row to bookmark it here for quick reference.</p>
        </div>
      `;
      return;
    }

    const favItems = CASTE_DATABASE.filter(item => state.favorites.has(item.id));

    DOM.drawerList.innerHTML = favItems.map(item => `
      <div class="surname-card" data-id="${item.id}" style="padding: 1rem;">
        <div class="card-top">
          <div class="card-title-group">
            <span class="card-devanagari" style="font-size: 1.25rem;">${escapeHtml(item.devanagari)}</span>
            <span class="card-roman" style="font-size: 0.85rem;">${escapeHtml(item.surname)}</span>
          </div>
          <button class="card-favorite-btn favorited" data-fav-id="${item.id}" title="Remove">❤️</button>
        </div>
        <div style="font-size: 0.8rem; color: var(--text-secondary); margin: 0.5rem 0;">
          <strong>${escapeHtml(item.community)}</strong> • Gotra: ${escapeHtml(item.gotra)}
        </div>
        <button class="card-view-btn" data-view-id="${item.id}">View Details ➔</button>
      </div>
    `).join('');
  }

  /**
   * Reset All Filters
   */
  function resetFilters() {
    state.searchQuery = '';
    state.selectedCategory = 'all';
    state.selectedCommunity = 'all';
    state.selectedGotra = 'all';
    state.selectedRegion = 'all';
    state.sortBy = 'surname-asc';
    state.page = 1;

    if (DOM.searchInput) DOM.searchInput.value = '';
    if (DOM.communityFilterSelect) DOM.communityFilterSelect.value = 'all';
    if (DOM.gotraFilterSelect) DOM.gotraFilterSelect.value = 'all';
    if (DOM.regionFilterSelect) DOM.regionFilterSelect.value = 'all';
    if (DOM.sortBySelect) DOM.sortBySelect.value = 'surname-asc';

    renderCategoryFilterBar();
    render();
    showToast('Filters reset to default');
  }

  /**
   * Toast Notification
   */
  function showToast(message) {
    if (!DOM.toastContainer) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    DOM.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  }

  /**
   * Utility to Escape HTML
   */
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /**
   * Event Binding
   */
  function bindEvents() {
    // Theme toggle
    if (DOM.themeToggleBtn) DOM.themeToggleBtn.addEventListener('click', toggleTheme);

    // Search Input
    if (DOM.searchInput) {
      DOM.searchInput.addEventListener('input', (e) => {
        state.searchQuery = e.target.value;
        state.page = 1;
        render();
      });
    }

    if (DOM.searchClearBtn) {
      DOM.searchClearBtn.addEventListener('click', () => {
        state.searchQuery = '';
        if (DOM.searchInput) DOM.searchInput.value = '';
        state.page = 1;
        render();
      });
    }

    // Category Filter Pills
    if (DOM.categoryFilterBar) {
      DOM.categoryFilterBar.addEventListener('click', (e) => {
        const pill = e.target.closest('.cat-pill');
        if (pill) {
          state.selectedCategory = pill.getAttribute('data-category');
          state.page = 1;
          renderCategoryFilterBar();
          render();
        }
      });
    }

    // Secondary Filter Dropdowns
    if (DOM.communityFilterSelect) {
      DOM.communityFilterSelect.addEventListener('change', (e) => {
        state.selectedCommunity = e.target.value;
        state.page = 1;
        render();
      });
    }

    if (DOM.gotraFilterSelect) {
      DOM.gotraFilterSelect.addEventListener('change', (e) => {
        state.selectedGotra = e.target.value;
        state.page = 1;
        render();
      });
    }

    if (DOM.regionFilterSelect) {
      DOM.regionFilterSelect.addEventListener('change', (e) => {
        state.selectedRegion = e.target.value;
        state.page = 1;
        render();
      });
    }

    if (DOM.sortBySelect) {
      DOM.sortBySelect.addEventListener('change', (e) => {
        state.sortBy = e.target.value;
        render();
      });
    }

    if (DOM.resetFiltersBtn) {
      DOM.resetFiltersBtn.addEventListener('click', resetFilters);
    }

    // View Mode Tabs
    const viewButtons = [
      { btn: DOM.viewGridBtn, mode: 'grid' },
      { btn: DOM.viewTableBtn, mode: 'table' },
      { btn: DOM.viewSagotraBtn, mode: 'sagotra' },
      { btn: DOM.viewCheckerBtn, mode: 'checker' },
      { btn: DOM.viewInsightsBtn, mode: 'insights' }
    ];

    viewButtons.forEach(({ btn, mode }) => {
      if (btn) {
        btn.addEventListener('click', () => {
          viewButtons.forEach(b => b.btn && b.btn.classList.remove('active'));
          btn.classList.add('active');
          state.viewMode = mode;
          render();
        });
      }
    });

    // Content Section Delegation (Card click, view click, favorite click)
    if (DOM.contentSection) {
      DOM.contentSection.addEventListener('click', (e) => {
        // Favorite button click
        const favBtn = e.target.closest('[data-fav-id]');
        if (favBtn) {
          e.stopPropagation();
          const id = favBtn.getAttribute('data-fav-id');
          toggleFavorite(id);
          return;
        }

        // View detail click or card click
        const card = e.target.closest('[data-id]');
        if (card) {
          const id = parseInt(card.getAttribute('data-id'), 10);
          const item = CASTE_DATABASE.find(x => x.id === id);
          if (item) {
            openDetailModal(item);
          }
        }
      });
    }

    // Load More Button
    if (DOM.loadMoreBtn) {
      DOM.loadMoreBtn.addEventListener('click', () => {
        state.page += 1;
        render();
      });
    }

    // Modal Close
    if (DOM.modalOverlay) {
      DOM.modalOverlay.addEventListener('click', (e) => {
        if (e.target === DOM.modalOverlay) {
          closeDetailModal();
        }
      });
    }

    // Drawer Open / Close
    if (DOM.favDrawerOpenBtn) DOM.favDrawerOpenBtn.addEventListener('click', openFavoritesDrawer);
    if (DOM.drawerCloseBtn) DOM.drawerCloseBtn.addEventListener('click', closeFavoritesDrawer);
    if (DOM.drawerOverlay) {
      DOM.drawerOverlay.addEventListener('click', (e) => {
        if (e.target === DOM.drawerOverlay) {
          closeFavoritesDrawer();
        }
      });
    }

    // Drawer delegation
    if (DOM.drawerList) {
      DOM.drawerList.addEventListener('click', (e) => {
        const favBtn = e.target.closest('[data-fav-id]');
        if (favBtn) {
          e.stopPropagation();
          const id = favBtn.getAttribute('data-fav-id');
          toggleFavorite(id);
          return;
        }

        const card = e.target.closest('[data-id]');
        if (card) {
          const id = parseInt(card.getAttribute('data-id'), 10);
          const item = CASTE_DATABASE.find(x => x.id === id);
          if (item) {
            closeFavoritesDrawer();
            openDetailModal(item);
          }
        }
      });
    }

    if (DOM.clearFavsBtn) {
      DOM.clearFavsBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear all saved favorites?')) {
          state.favorites.clear();
          localStorage.removeItem('nepal_surnames_favs');
          updateFavBadge();
          renderFavoritesDrawer();
          render();
          showToast('Cleared all favorites');
        }
      });
    }

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
      if ((e.key === '/' || (e.ctrlKey && e.key === 'k')) && document.activeElement !== DOM.searchInput) {
        e.preventDefault();
        DOM.searchInput.focus();
      } else if (e.key === 'Escape') {
        if (DOM.modalOverlay.classList.contains('active')) {
          closeDetailModal();
        } else if (DOM.drawerOverlay.classList.contains('active')) {
          closeFavoritesDrawer();
        }
      }
    });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
