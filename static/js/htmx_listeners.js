// Listens for server-sent HX-Trigger events and refreshes containers with `data-refresh-url`.
(function () {
  function refreshContainers() {
    const nodes = document.querySelectorAll('[data-refresh-url]');
    nodes.forEach(node => {
      const url = node.getAttribute('data-refresh-url');
      if (url) {
        // use htmx to swap the content
        htmx.ajax('GET', url, {target: node, swap: 'innerHTML'});
      }
    });
  }

  // Close bootstrap modal if open (call when a 204 success triggers an event)
  function closeModalIfOpen() {
    const modalEl = document.getElementById('modal');
    if (!modalEl) return;
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    if (modalInstance) {
      modalInstance.hide();
    }
  }

  ['ticketListUpdated', 'ticketUpdated', 'invitationSent'].forEach(evtName => {
    document.body.addEventListener(evtName, function () {
      closeModalIfOpen();
      refreshContainers();
    });
  });
})();
