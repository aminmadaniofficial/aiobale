// Aiobale Documentation App Engine
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  initSearch();
  initCopyButtons();
  initScrollSpy();
});

// 1. Theme Management (Dark / Light)
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const savedTheme = localStorage.getItem('aiobale-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('aiobale-theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }
}

function updateThemeIcon(theme) {
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) return;

  if (theme === 'light') {
    themeToggle.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path>
      </svg>
    `;
    themeToggle.setAttribute('title', 'تغییر به تم تاریک');
  } else {
    themeToggle.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="4"></circle>
        <path d="M12 2v2"></path>
        <path d="M12 20v2"></path>
        <path d="m4.93 4.93 1.41 1.41"></path>
        <path d="m17.66 17.66 1.41 1.41"></path>
        <path d="M2 12h2"></path>
        <path d="M20 12h2"></path>
        <path d="m6.34 17.66-1.41 1.41"></path>
        <path d="m19.07 4.93-1.41 1.41"></path>
      </svg>
    `;
    themeToggle.setAttribute('title', 'تغییر به تم روشن');
  }
}

// 2. Mobile Responsive Sidebar Drawer
function initSidebar() {
  const mobileToggle = document.getElementById('mobile-menu-toggle') || document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  const navLinks = document.querySelectorAll('.sidebar-link');

  function openSidebar() {
    sidebar.classList.add('mobile-open');
    if (backdrop) backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar.classList.remove('mobile-open');
    if (backdrop) backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (mobileToggle) {
    mobileToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      if (sidebar.classList.contains('mobile-open')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', closeSidebar);
  }

  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 1024) {
        closeSidebar();
      }
    });
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 1024 && sidebar.classList.contains('mobile-open')) {
      closeSidebar();
    }
  });
}

// 3. Search Engine (Modal & Live Search)
function initSearch() {
  const searchBtn = document.getElementById('search-btn') || document.getElementById('doc-search');
  const searchModal = document.getElementById('search-modal');
  const modalInput = document.getElementById('search-input') || document.getElementById('modal-search-input');
  const resultsContainer = document.getElementById('search-results');

  const index = [];

  // Index sections
  document.querySelectorAll('.doc-section').forEach((section) => {
    const titleEl = section.querySelector('.section-title');
    const title = titleEl ? titleEl.innerText.trim() : '';
    const sectionId = section.getAttribute('id');
    const descEl = section.querySelector('.section-subtitle') || section.querySelector('.section-desc');
    const desc = descEl ? descEl.innerText.trim() : '';

    if (title && sectionId) {
      index.push({
        id: sectionId,
        title: title,
        desc: desc || 'بخش اصلی مستندات',
        type: 'بخش اصلی',
        keywords: `${title} ${desc} ${sectionId}`,
      });
    }

    // Index subheadings
    section.querySelectorAll('h3.sub-heading, h3.sub-title, h4').forEach((heading) => {
      const hText = heading.innerText.trim();
      const hId = heading.id || sectionId;
      if (hText) {
        index.push({
          id: hId,
          title: hText,
          desc: `در ${title}`,
          type: 'موضوع',
          keywords: `${hText} ${title} ${hId}`,
        });
      }
    });

    // Index ALL table rows in API tables
    section.querySelectorAll('.api-table tbody tr').forEach((row) => {
      const cells = row.querySelectorAll('td');
      if (cells.length >= 3) {
        const methodCode = cells[0].querySelector('code') ? cells[0].querySelector('code').innerText.trim() : cells[0].innerText.trim();
        const params = cells[1].innerText.trim();
        const desc = cells[2].innerText.trim();
        const rowId = row.id || sectionId;

        index.push({
          id: rowId,
          title: methodCode,
          desc: `${desc} (پارامترها: ${params || 'ندارد'})`,
          type: 'متد API',
          keywords: `${methodCode} ${params} ${desc} ${title} کیف پول wallet kifpool کارت حساب هدیه عیدی gift`,
        });
      }
    });
  });

  function openSearchModal() {
    if (!searchModal) return;
    searchModal.classList.add('open', 'active');
    if (modalInput) {
      modalInput.value = '';
      setTimeout(() => modalInput.focus(), 60);
      renderResults('');
    }
    document.body.style.overflow = 'hidden';
  }

  function closeSearchModal() {
    if (!searchModal) return;
    searchModal.classList.remove('open', 'active');
    document.body.style.overflow = '';
  }

  if (searchBtn) {
    searchBtn.addEventListener('click', (e) => {
      e.preventDefault();
      openSearchModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (searchModal && (searchModal.classList.contains('open') || searchModal.classList.contains('active'))) {
        closeSearchModal();
      } else {
        openSearchModal();
      }
    }
    if (e.key === 'Escape' && searchModal && (searchModal.classList.contains('open') || searchModal.classList.contains('active'))) {
      closeSearchModal();
    }
  });

  if (searchModal) {
    searchModal.addEventListener('click', (e) => {
      if (e.target === searchModal) {
        closeSearchModal();
      }
    });
  }

  if (modalInput) {
    modalInput.addEventListener('input', (e) => {
      renderResults(e.target.value);
    });
  }

  function renderResults(query) {
    if (!resultsContainer) return;
    const cleanQuery = query.trim().toLowerCase();

    if (!cleanQuery) {
      resultsContainer.innerHTML = `
        <div style="text-align: center; padding: 28px 16px; color: var(--text-muted); font-size: 0.9rem;">
          عبارت مورد نظر (مانند get_wallet، کیف پول، send_message، FSM، دکمه، فیلتر) را جستجو کنید...
        </div>
      `;
      return;
    }

    const matched = index.filter((item) => {
      const q = cleanQuery;
      return (
        item.title.toLowerCase().includes(q) ||
        item.desc.toLowerCase().includes(q) ||
        (item.keywords && item.keywords.toLowerCase().includes(q))
      );
    });

    if (matched.length === 0) {
      resultsContainer.innerHTML = `
        <div style="text-align: center; padding: 28px 16px; color: var(--text-muted); font-size: 0.9rem;">
          نتیجه‌ای برای «<strong>${escapeHtml(cleanQuery)}</strong>» یافت نشد.
        </div>
      `;
      return;
    }

    resultsContainer.innerHTML = matched
      .slice(0, 15)
      .map((item) => {
        return `
        <li>
          <a href="#${item.id}" class="search-result-item" onclick="document.getElementById('search-modal').classList.remove('open', 'active'); document.body.style.overflow='';">
            <div>
              <span style="display: inline-block; font-size: 0.72rem; padding: 2px 6px; border-radius: 4px; background: var(--bg-tertiary); color: var(--text-muted); margin-bottom: 4px;">${escapeHtml(item.type)}</span>
              <div style="font-weight: 600; font-size: 0.95rem; color: var(--text-primary);">${highlightText(item.title, cleanQuery)}</div>
              <div style="font-size: 0.82rem; color: var(--text-muted);">${highlightText(item.desc, cleanQuery)}</div>
            </div>
            <div style="color: var(--text-muted);">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m15 18-6-6 6-6"/>
              </svg>
            </div>
          </a>
        </li>
      `;
      })
      .join('');
  }

  function highlightText(text, query) {
    if (!query) return escapeHtml(text);
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return escapeHtml(text).replace(regex, '<mark style="background: rgba(37,99,235,0.25); color: var(--text-link); border-radius: 2px; padding: 0 2px;">$1</mark>');
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
}

// 4. Code Block Copy Buttons
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const container = btn.closest('.code-container');
      const code = container ? container.querySelector('pre').innerText : '';
      if (!code) return;

      try {
        await navigator.clipboard.writeText(code);
        btn.classList.add('copied');
        const textSpan = btn.querySelector('.copy-text');
        if (textSpan) textSpan.innerText = 'کپی شد!';
        setTimeout(() => {
          btn.classList.remove('copied');
          if (textSpan) textSpan.innerText = 'کپی';
        }, 2000);
      } catch (err) {
        console.error('Failed to copy text', err);
      }
    });
  });
}

// 5. ScrollSpy & Sidebar Active State (Exact Element Matching)
function initScrollSpy() {
  const navLinks = Array.from(document.querySelectorAll('.sidebar-link'));
  const targets = [];

  navLinks.forEach((link) => {
    const href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      const id = href.substring(1);
      const el = document.getElementById(id);
      if (el) {
        targets.push({ id, el, link });
      }
    }
  });

  function updateActiveLink() {
    const scrollPos = window.scrollY + 140;
    let currentId = null;

    for (let i = targets.length - 1; i >= 0; i--) {
      const item = targets[i];
      const top = item.el.getBoundingClientRect().top + window.scrollY;
      if (scrollPos >= top - 20) {
        currentId = item.id;
        break;
      }
    }

    if (!currentId && targets.length > 0 && window.scrollY < 200) {
      currentId = targets[0].id;
    }

    targets.forEach((item) => {
      if (item.id === currentId) {
        item.link.classList.add('active');
      } else {
        item.link.classList.remove('active');
      }
    });
  }

  window.addEventListener('scroll', updateActiveLink, { passive: true });
  updateActiveLink();

  // Add instant active state toggle on direct click
  navLinks.forEach((link) => {
    link.addEventListener('click', function () {
      navLinks.forEach((l) => l.classList.remove('active'));
      this.classList.add('active');
    });
  });
}
