(function () {
  'use strict';

  function initIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  function initSidebar() {
    var sidebar = document.getElementById('appSidebar');
    var backdrop = document.getElementById('sidebarBackdrop');
    var openBtn = document.getElementById('sidebarOpenBtn');
    var closeBtn = document.getElementById('sidebarCloseBtn');
    if (!sidebar) return;

    function setOpen(open) {
      sidebar.classList.toggle('is-open', open);
      if (backdrop) backdrop.classList.toggle('is-open', open);
      if (openBtn) openBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    }

    if (openBtn) openBtn.addEventListener('click', function () { setOpen(true); });
    if (closeBtn) closeBtn.addEventListener('click', function () { setOpen(false); });
    if (backdrop) backdrop.addEventListener('click', function () { setOpen(false); });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && sidebar.classList.contains('is-open')) {
        setOpen(false);
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1024 && sidebar.classList.contains('is-open')) {
        setOpen(false);
      }
    });
  }

  function initUserDropdown() {
    var dropdown = document.getElementById('userDropdown');
    var trigger = document.getElementById('userDropdownTrigger');
    if (!dropdown || !trigger) return;

    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !dropdown.classList.contains('is-open');
      dropdown.classList.toggle('is-open', open);
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    document.addEventListener('click', function (e) {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove('is-open');
        trigger.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        dropdown.classList.remove('is-open');
        trigger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  function initPasswordToggles() {
    var buttons = document.querySelectorAll('[data-toggle-password]');
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var targetId = btn.getAttribute('data-toggle-password');
        var input = document.getElementById(targetId);
        if (!input) return;
        var isHidden = input.type === 'password';
        input.type = isHidden ? 'text' : 'password';
        btn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
        btn.setAttribute('aria-pressed', isHidden ? 'true' : 'false');
        var eye = btn.querySelector('.icon-eye');
        var eyeOff = btn.querySelector('.icon-eye-off');
        if (eye && eyeOff) {
          eye.style.display = isHidden ? 'none' : 'block';
          eyeOff.style.display = isHidden ? 'block' : 'none';
        }
      });
    });
  }

  function initTableFilters() {
    var containers = document.querySelectorAll('[data-filter-table]');
    containers.forEach(function (container) {
      var searchInput = container.querySelector('[data-table-search]');
      var pills = container.querySelectorAll('[data-status-filter]');
      var rows = container.querySelectorAll('tbody tr[data-row]');
      var noMatch = container.querySelector('[data-no-match]');
      var activeStatus = 'all';

      function applyFilter() {
        var q = searchInput ? searchInput.value.trim().toLowerCase() : '';
        var visible = 0;
        rows.forEach(function (row) {
          var text = (row.textContent || '').toLowerCase();
          var status = (row.getAttribute('data-status') || '').toLowerCase();
          var matchSearch = !q || text.indexOf(q) !== -1;
          var matchStatus = activeStatus === 'all' || status === activeStatus;
          var show = matchSearch && matchStatus;
          row.style.display = show ? '' : 'none';
          if (show) visible++;
        });
        if (noMatch) {
          noMatch.style.display = (rows.length > 0 && visible === 0) ? 'block' : 'none';
        }
      }

      if (searchInput) {
        searchInput.addEventListener('input', applyFilter);
      }

      pills.forEach(function (pill) {
        pill.addEventListener('click', function () {
          pills.forEach(function (p) { p.classList.remove('is-active'); });
          pill.classList.add('is-active');
          activeStatus = pill.getAttribute('data-status-filter') || 'all';
          applyFilter();
        });
      });
    });
  }

  function initColorSwatches() {
    var map = {
      gold: '#D4A037',
      kuningan: '#C8923B',
      silver: '#B8C0CC',
      chrome: '#CBD5E1',
      putih: '#F8FAFC',
      white: '#F8FAFC',
      abu: '#8C95A4',
      grey: '#8C95A4',
      gray: '#8C95A4',
      hitam: '#1F2937',
      black: '#1F2937',
      biru: '#2563EB',
      blue: '#2563EB',
      merah: '#DC2626',
      red: '#DC2626',
      hijau: '#16A34A',
      green: '#16A34A'
    };
    document.querySelectorAll('[data-color-swatch]').forEach(function (el) {
      var val = (el.getAttribute('data-color-swatch') || '').trim().toLowerCase();
      el.style.backgroundColor = map[val] || '#B87D28';
    });
  }

  function initSubmitLoading() {
    document.querySelectorAll('form[data-loading-form]').forEach(function (form) {
      form.addEventListener('submit', function () {
        var btn = form.querySelector('button[type="submit"]');
        if (btn && !btn.disabled) {
          btn.disabled = true;
          btn.style.opacity = '0.8';
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initIcons();
    initSidebar();
    initUserDropdown();
    initPasswordToggles();
    initTableFilters();
    initColorSwatches();
    initSubmitLoading();
  });
})();

(function () {
  'use strict';

  function initFlashDismiss() {
    document.querySelectorAll('[data-dismiss-flash]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var alert = btn.closest('.flash-alert');
        if (alert) alert.remove();
      });
    });
  }

  function initConfirmDeleteModal() {
    var overlay = document.getElementById('confirmDeleteModal');
    var msgEl = document.getElementById('confirmDeleteMessage');
    var cancelBtn = document.getElementById('confirmDeleteCancel');
    var confirmBtn = document.getElementById('confirmDeleteSubmit');
    if (!overlay || !confirmBtn) return;

    var pendingForm = null;

    function close() {
      overlay.classList.remove('is-open');
      pendingForm = null;
    }

    document.querySelectorAll('form[data-confirm-delete]').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        if (form.getAttribute('data-confirmed') === 'true') return;
        e.preventDefault();
        pendingForm = form;
        if (msgEl) {
          msgEl.textContent = form.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this record?';
        }
        overlay.classList.add('is-open');
        confirmBtn.focus();
      });
    });

    confirmBtn.addEventListener('click', function () {
      if (pendingForm) {
        pendingForm.setAttribute('data-confirmed', 'true');
        pendingForm.submit();
      }
    });

    if (cancelBtn) cancelBtn.addEventListener('click', close);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('is-open')) close();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initFlashDismiss();
    initConfirmDeleteModal();
  });
})();
