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
  const sunIcon = document.getElementById('sun-icon');
  const moonIcon = document.getElementById('moon-icon');
  if (!sunIcon || !moonIcon) return;
  if (theme === 'dark') {
    sunIcon.style.display = 'block';
    moonIcon.style.display = 'none';
  } else {
    sunIcon.style.display = 'none';
    moonIcon.style.display = 'block';
  }
}

// 2. Sidebar Navigation & Mobile Drawer
function initSidebar() {
  const menuToggle = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 960 && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
          sidebar.classList.remove('open');
        }
      }
    });

    // Close on link click on mobile
    sidebar.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 960) {
          sidebar.classList.remove('open');
        }
      });
    });
  }
}

// 3. Search Engine
const searchIndex = [
  { title: "معرفی و شروع سریع (Getting Started)", id: "getting-started", category: "مقدمه" },
  { title: "نصب و پیش‌نیازها (Installation)", id: "installation", category: "شروع" },
  { title: "اولین ربات در ۵ دقیقه (Quickstart)", id: "quickstart", category: "شروع" },
  { title: "احراز هویت و مدیریت سشن (Authentication)", id: "authentication", category: "هسته" },
  { title: "ورود با CLI و شماره تلفن (Phone Login)", id: "phone-login", category: "احراز هویت" },
  { title: "ورود با توکن پایدار (Token Auth)", id: "token-auth", category: "احراز هویت" },
  { title: "اجرا در محیط‌های Headless و داکر", id: "headless-auth", category: "احراز هویت" },
  { title: "معماری کلاینت و چرخه حیات (Client)", id: "client-architecture", category: "کلاینت" },
  { title: "پیکربندی کلاینت (Client Configuration)", id: "client-config", category: "کلاینت" },
  { title: "اتصال مجدد خودکار (Auto Reconnect)", id: "client-reconnect", category: "کلاینت" },
  { title: "دیسپچر و مسیریابی رویدادها (Dispatcher)", id: "dispatcher", category: "رویدادها" },
  { title: "مدیریت پیام و رویدادها (@dp.message)", id: "dp-handlers", category: "رویدادها" },
  { title: "روترهای ماژولار (Sub-Routers)", id: "routers", category: "رویدادها" },
  { title: "تزریق وابستگی (Dependency Injection)", id: "dependency-injection", category: "رویدادها" },
  { title: "فیلترها و Magic Filter (Filters & F)", id: "filters", category: "فیلترها" },
  { title: "مجیک فیلتر F (Magic Filter)", id: "magic-filter", category: "فیلترها" },
  { title: "فیلترهای پیش‌ساخته (IsText, IsDocument, ...)", id: "builtin-filters", category: "فیلترها" },
  { title: "ترکیب فیلترها (and_f, or_f, invert_f)", id: "logic-filters", category: "فیلترها" },
  { title: "فیلترهای سفارشی (Custom Filters)", id: "custom-filters", category: "فیلترها" },
  { title: "مرجع متدهای پیام‌رسانی (Messaging API)", id: "api-messaging", category: "API RPC" },
  { title: "send_message (ارسال پیام متنی)", id: "method-send-message", category: "پیام‌رسانی" },
  { title: "send_photo / send_document (ارسال مدیا)", id: "method-send-media", category: "پیام‌رسانی" },
  { title: "send_voice / send_audio / send_video", id: "method-send-audio-video", category: "پیام‌رسانی" },
  { title: "edit_message / delete_message / pin_message", id: "method-edit-delete-pin", category: "پیام‌رسانی" },
  { title: "forward_message / clear_chat / delete_chat", id: "method-forward-clear", category: "پیام‌رسانی" },
  { title: "مرجع متدهای گروه‌ها و کانال‌ها (Groups API)", id: "api-groups", category: "API RPC" },
  { title: "create_group / get_full_group", id: "method-create-group", category: "گروه و کانال" },
  { title: "kick_user / unban_user / get_banned_users", id: "method-kick-ban", category: "مدیریت گروه" },
  { title: "make_user_admin / set_member_permissions", id: "method-permissions", category: "مدیریت گروه" },
  { title: "get_group_invite_url / join_group", id: "method-group-links", category: "گروه و کانال" },
  { title: "مرجع متدهای کاربران و مخاطبین (Users API)", id: "api-users", category: "API RPC" },
  { title: "get_contacts / add_contact / import_contacts", id: "method-contacts", category: "کاربران" },
  { title: "block_user / unblock_user / load_users", id: "method-block-users", category: "کاربران" },
  { title: "edit_name / edit_about / edit_nickname", id: "method-edit-profile", category: "پروفایل" },
  { title: "مرجع واکنش‌ها و آمار (Abacus API)", id: "api-abacus", category: "واکنش و بازدید" },
  { title: "مرجع وضعیت و تایپینگ (Presence API)", id: "api-presence", category: "وضعیت آنلاین" },
  { title: "مرجع فایل‌ها و دانلود/آپلود (Files API)", id: "api-files", category: "فایل و رسانه" },
  { title: "مرجع تایپ‌ها و مدل‌های داده (Types Reference)", id: "types-reference", category: "مدل‌های داده" },
  { title: "کلاس Message و متدهای پاسخ کمکی", id: "type-message", category: "مدل داده" },
  { title: "کلاس‌های Chat, User, Member, FullGroup", id: "type-chat-user", category: "مدل داده" },
  { title: "مرجع انام‌ها و ثابت‌ها (Enums Reference)", id: "enums-reference", category: "ثابت‌ها" },
  { title: "ChatType, PeerType, TypingMode, AuthErrors", id: "enums-details", category: "ثابت‌ها" },
  { title: "پروژه ۱: ربات اکو و پاسخگوی هوشمند", id: "example-echo", category: "پروژه‌های عملی" },
  { title: "پروژه ۲: ربات مدیریت گروه و ضداسپم", id: "example-admin", category: "پروژه‌های عملی" },
  { title: "پروژه ۳: ربات دانلودر و آپلودر مدیا", id: "example-downloader", category: "پروژه‌های عملی" },
  { title: "پروژه ۴: ربات برودکست و زمان‌بندی کانال", id: "example-broadcast", category: "پروژه‌های عملی" },
  { title: "پروژه ۵: معماری چندروتر و دکمه‌های اینلاین", id: "example-routers", category: "پروژه‌های عملی" },
  { title: "مدیریت خطاها و عیب‌یابی (Troubleshooting)", id: "troubleshooting", category: "خطاها" },
];

function initSearch() {
  const searchBtn = document.getElementById('search-btn');
  const searchModal = document.getElementById('search-modal');
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');

  if (!searchBtn || !searchModal || !searchInput || !searchResults) return;

  function openSearch() {
    searchModal.classList.add('open');
    searchInput.value = '';
    renderResults(searchIndex.slice(0, 8));
    setTimeout(() => searchInput.focus(), 50);
  }

  function closeSearch() {
    searchModal.classList.remove('open');
  }

  searchBtn.addEventListener('click', openSearch);

  searchModal.addEventListener('click', (e) => {
    if (e.target === searchModal) closeSearch();
  });

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      searchModal.classList.contains('open') ? closeSearch() : openSearch();
    } else if (e.key === 'Escape' && searchModal.classList.contains('open')) {
      closeSearch();
    } else if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
      e.preventDefault();
      openSearch();
    }
  });

  searchInput.addEventListener('input', (e) => {
    const q = e.target.value.trim().toLowerCase();
    if (!q) {
      renderResults(searchIndex.slice(0, 8));
      return;
    }
    const filtered = searchIndex.filter(item => 
      item.title.toLowerCase().includes(q) || 
      item.id.toLowerCase().includes(q) || 
      item.category.toLowerCase().includes(q)
    );
    renderResults(filtered);
  });

  function renderResults(items) {
    searchResults.innerHTML = '';
    if (items.length === 0) {
      searchResults.innerHTML = '<li style="padding: 20px; text-align: center; color: var(--text-muted);">موردی یافت نشد.</li>';
      return;
    }
    items.forEach(item => {
      const li = document.createElement('li');
      li.className = 'search-result-item';
      li.innerHTML = `
        <span class="search-result-title">${item.title}</span>
        <span class="search-result-category">${item.category}</span>
      `;
      li.addEventListener('click', () => {
        closeSearch();
        const target = document.getElementById(item.id);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
          history.pushState(null, null, `#${item.id}`);
        }
      });
      searchResults.appendChild(li);
    });
  }
}

// 4. Copy Code to Clipboard
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

// 5. ScrollSpy & Sidebar Active State
function initScrollSpy() {
  const sections = document.querySelectorAll('.doc-section');
  const navLinks = document.querySelectorAll('.sidebar-link');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollPos = window.scrollY + 120;

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove('active');
      if (current && link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });
}
