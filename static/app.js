// Additional JavaScript for enhanced UX
document.addEventListener('DOMContentLoaded', function () {
	// Add smooth transitions for HTMX requests
	document.body.addEventListener('htmx:beforeRequest', function (evt) {
		const target = evt.target;
		target.style.transition = 'opacity 0.2s ease-in-out';
		target.style.opacity = '0.7';

		// Hide refresh icon and show spinner for refresh buttons
		const refreshIcon = target.querySelector('.refresh-icon');
		const buttonText = target.querySelector('.button-text');
		if (refreshIcon) {
			refreshIcon.style.display = 'none';
		}
		if (buttonText) {
			buttonText.style.opacity = '0.7';
		}
	});

	document.body.addEventListener('htmx:afterRequest', function (evt) {
		const target = evt.target;
		target.style.opacity = '1';

		// Show refresh icon and hide spinner for refresh buttons
		const refreshIcon = target.querySelector('.refresh-icon');
		const buttonText = target.querySelector('.button-text');
		if (refreshIcon) {
			refreshIcon.style.display = 'block';
		}
		if (buttonText) {
			buttonText.style.opacity = '1';
		}
	});

	// Auto-refresh functionality (optional)
	let autoRefreshInterval;

	function startAutoRefresh() {
		autoRefreshInterval = setInterval(() => {
			const activeContent = document.querySelector('#content [hx-get]');
			if (activeContent) {
				htmx.trigger(activeContent, 'click');
			}
		}, 30000); // Refresh every 30 seconds
	}

	function stopAutoRefresh() {
		if (autoRefreshInterval) {
			clearInterval(autoRefreshInterval);
		}
	}

	// Add keyboard shortcuts
	document.addEventListener('keydown', function (e) {
		// Press 'r' to refresh current view
		if (e.key === 'r' && !e.ctrlKey && !e.metaKey) {
			const activeButton = document.querySelector('#content button[hx-get]');
			if (activeButton) {
				activeButton.click();
			}
		}

		// Press 'h' to go home
		if (e.key === 'h' && !e.ctrlKey && !e.metaKey) {
			window.location.href = '/';
		}
	});
});