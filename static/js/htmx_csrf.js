// Simple HTMX CSRF helper. Ensures htmx requests include CSRF token.
(function () {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  document.body.addEventListener('htmx:configRequest', function (event) {
    const token = getCookie('csrftoken');
    if (token) {
      event.detail.headers['X-CSRFToken'] = token;
    }
  });
})();
