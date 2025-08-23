document.addEventListener('DOMContentLoaded', function () {
    // Format RUT input
    const rutInput = document.getElementById('rut');
    if (rutInput) {
        rutInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/[^0-9kK.-]/g, '');
            value = value.replace(/\./g, '').replace(/-/g, '');

            if (value.length > 1) {
                let body = value.slice(0, -1);
                let dv = value.slice(-1).toUpperCase();
                body = new Intl.NumberFormat('es-CL').format(body);
                e.target.value = `${body}-${dv}`;
            } else {
                e.target.value = value;
            }
        });
    }

    // 1. Column Visibility
    const table = document.getElementById('tickets-table');
    if (!table) return;

    const columnToggles = document.getElementById('column-toggles');
    const headers = table.querySelectorAll('thead th');
    const columnNames = Array.from(headers).map(th => th.dataset.columnName).filter(Boolean);

    columnNames.forEach((name, index) => {
        const colIndex = Array.from(headers).findIndex(h => h.dataset.columnName === name);
        
        const label = document.createElement('label');
        label.className = 'flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'mr-2';
        checkbox.checked = true;
        checkbox.dataset.columnIndex = colIndex;

        checkbox.addEventListener('change', (e) => {
            const idx = e.target.dataset.columnIndex;
            const cells = table.querySelectorAll(`th:nth-child(${parseInt(idx) + 1}), td:nth-child(${parseInt(idx) + 1})`);
            cells.forEach(cell => {
                cell.style.display = e.target.checked ? '' : 'none';
            });
        });

        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(name));
        if (columnToggles) {
            columnToggles.appendChild(label);
        }
    });

    // 2. Table Sorting
    headers.forEach(header => {
        if (header.dataset.sortKey) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const sortKey = header.dataset.sortKey;
                const currentUrl = new URL(window.location.href);
                const currentSort = currentUrl.searchParams.get('sort_by');
                const currentOrder = currentUrl.searchParams.get('sort_dir') || 'asc';
                
                let newOrder = 'asc';
                if (currentSort === sortKey && currentOrder === 'asc') {
                    newOrder = 'desc';
                }
                
                currentUrl.searchParams.set('sort_by', sortKey);
                currentUrl.searchParams.set('sort_dir', newOrder);
                window.location.href = currentUrl.toString();
            });
        }
    });

    // 3. Real-time Countdown Timers
    const countdownTimers = document.querySelectorAll('.countdown-timer');

    function updateTimers() {
        countdownTimers.forEach(timer => {
            const fpaString = timer.dataset.fpa;
            if (!fpaString) return;

            const fpaDate = new Date(fpaString);
            const now = new Date();
            let totalSeconds = Math.floor((fpaDate - now) / 1000);

            if (totalSeconds < 0) {
                timer.textContent = 'Vencido';
                timer.className = 'countdown-timer text-sm font-medium text-red-600';
                return;
            }

            let days = Math.floor(totalSeconds / (3600 * 24));
            totalSeconds %= (3600 * 24);
            let hours = Math.floor(totalSeconds / 3600);
            totalSeconds %= 3600;
            let minutes = Math.floor(totalSeconds / 60);
            let seconds = totalSeconds % 60;

            let displayText = '';
            if (days > 0) {
                displayText += `${days}d `;
            }
            displayText += `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            timer.textContent = displayText;

            let colorClass = 'text-orange-600'; // Default for < 1 hour
            const totalHours = (days * 24) + hours;
            if (totalHours > 24) {
                colorClass = 'text-green-600';
            } else if (totalHours > 1) {
                colorClass = 'text-yellow-600';
            }
            timer.className = `countdown-timer text-sm font-medium ${colorClass}`;
        });
    }

    if (countdownTimers.length > 0) {
        setInterval(updateTimers, 1000);
        updateTimers(); // Initial call
    }
});