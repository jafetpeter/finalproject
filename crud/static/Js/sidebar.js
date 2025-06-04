document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('logo-sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const toggleButton = document.getElementById('mobile-menu-button');

  function toggleSidebar() {
      sidebar.classList.toggle('-translate-x-full');
      overlay.classList.toggle('hidden');
  }

  toggleButton.addEventListener('click', toggleSidebar);
  overlay.addEventListener('click', toggleSidebar);
});