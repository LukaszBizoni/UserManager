(function () {
  "use strict";

  const storageKey = "cadastro-clientes-theme";
  const root = document.documentElement;

  function readStoredTheme() {
    try {
      return window.localStorage.getItem(storageKey);
    } catch (_error) {
      return null;
    }
  }

  function storeTheme(theme) {
    try {
      window.localStorage.setItem(storageKey, theme);
    } catch (_error) {
      // O tema continua funcionando durante a navegação atual sem armazenamento.
    }
  }

  function normalizeTheme(theme) {
    return theme === "light" ? "light" : "dark";
  }

  function updateToggle(theme) {
    const button = document.getElementById("theme-toggle");
    const icon = document.getElementById("theme-icon");
    const label = document.getElementById("theme-label");

    if (!button || !icon || !label) {
      return;
    }

    const darkThemeIsActive = theme === "dark";
    const actionLabel = darkThemeIsActive ? "Ativar tema claro" : "Ativar tema escuro";

    icon.textContent = darkThemeIsActive ? "☀" : "☾";
    label.textContent = darkThemeIsActive ? "Tema claro" : "Tema escuro";
    button.setAttribute("aria-label", actionLabel);
    button.setAttribute("title", actionLabel);
  }

  function applyTheme(theme) {
    const selectedTheme = normalizeTheme(theme);
    root.setAttribute("data-bs-theme", selectedTheme);
    updateToggle(selectedTheme);
  }

  applyTheme(readStoredTheme());

  document.addEventListener("DOMContentLoaded", function () {
    applyTheme(root.getAttribute("data-bs-theme"));

    const button = document.getElementById("theme-toggle");
    if (!button) {
      return;
    }

    button.addEventListener("click", function () {
      const currentTheme = normalizeTheme(root.getAttribute("data-bs-theme"));
      const nextTheme = currentTheme === "dark" ? "light" : "dark";

      storeTheme(nextTheme);
      applyTheme(nextTheme);
    });
  });
})();
