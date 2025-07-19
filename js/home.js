function toggleDashboard() {
  const dash = document.getElementById("dashboard");
  dash.classList.toggle("show");
}


function switchTab(tab) {
  // Remove active-tab class from both
  document.getElementById('upcoming_events').classList.remove('active-tab');
  document.getElementById('live_events').classList.remove('active-tab');

  // Hide both content areas
  document.getElementById('upcoming_tab').style.display = 'none';
  document.getElementById('live_tab').style.display = 'none';

  // Show selected tab and mark active
  if (tab === 'upcoming') {
    document.getElementById('upcoming_events').classList.add('active-tab');
    document.getElementById('upcoming_tab').style.display = 'block';
  } else {
    document.getElementById('live_events').classList.add('active-tab');
    document.getElementById('live_tab').style.display = 'block';
  }
}
