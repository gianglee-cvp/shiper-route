// Map Optimization & Logic
const map = L.map('map').setView([21.0285, 105.8542], 13);

// Dark Mode Map Filter (CartoDB Dark Matter is good but let's stick to standard and filter if needed, or use specific provider)
// Using OpenStreetMap but detailed
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Variables
let startMarker = null;
let endMarker = null;
let startGhost = null; // Shows where user clicked loosely
let endGhost = null;
let routeLine = null;
let selectionMode = null; // 'start' or 'end'

// Click Handler
map.on('click', async function (e) {
    if (!selectionMode) return;

    const clickedLat = e.latlng.lat;
    const clickedLng = e.latlng.lng;

    updateStatus("Đang tìm điểm gần nhất trên bản đồ...");

    try {
        // Get nearest node from backend
        const response = await fetch('http://localhost:5000/nearest-node', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                lat: clickedLat,
                lng: clickedLng
            })
        });

        const data = await response.json();

        if (data.error) {
            updateStatus(`Lỗi: ${data.error}`);
            return;
        }

        // Use the nearest node coordinates
        const lat = data.lat;
        const lng = data.lng;
        const nodeId = data.id;
        const coordsStr = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;

        if (selectionMode === 'start') {
            // Remove old markers
            if (startMarker) map.removeLayer(startMarker);
            if (startGhost) map.removeLayer(startGhost);

            // Add ghost marker (click point)
            startGhost = L.circleMarker([clickedLat, clickedLng], {
                color: '#9ca3af',
                fillColor: '#9ca3af',
                fillOpacity: 0.5,
                radius: 4,
                interactive: false
            }).addTo(map);

            // Add real marker (snapped node)
            startMarker = L.circleMarker([lat, lng], {
                color: '#3b82f6',       // Blue border
                fillColor: '#3b82f6',   // Blue fill
                fillOpacity: 0.8,
                radius: 8
            }).addTo(map);

            // Draw line between ghost and real? optional, maybe too cluttered. 
            // Let's just keep them distinct.

            document.getElementById('start-coords').innerText = coordsStr + " (Node)";
            document.getElementById('start-coords').dataset.lat = lat;
            document.getElementById('start-coords').dataset.lng = lng;
            document.getElementById('start-coords').dataset.nodeid = nodeId;

        } else if (selectionMode === 'end') {
            if (endMarker) map.removeLayer(endMarker);
            if (endGhost) map.removeLayer(endGhost);

            endGhost = L.circleMarker([clickedLat, clickedLng], {
                color: '#9ca3af',
                fillColor: '#9ca3af',
                fillOpacity: 0.5,
                radius: 4,
                interactive: false
            }).addTo(map);

            endMarker = L.circleMarker([lat, lng], {
                color: '#ef4444',       // Red border (Tailwind red-500)
                fillColor: '#ef4444',   // Red fill
                fillOpacity: 0.8,
                radius: 8
            }).addTo(map);

            document.getElementById('end-coords').innerText = coordsStr + " (Node)";
            document.getElementById('end-coords').dataset.lat = lat;
            document.getElementById('end-coords').dataset.lng = lng;
            document.getElementById('end-coords').dataset.nodeid = nodeId;
        }

        selectionMode = null; // Reset mode
        document.body.style.cursor = 'default';
        updateStatus("Đã chọn điểm nút giao thông gần nhất!");

    } catch (err) {
        console.error(err);
        updateStatus("Không thể kết nối đến server để lấy điểm gần nhất.");
    }
});

function setMode(mode) {
    selectionMode = mode;
    document.body.style.cursor = 'crosshair';
    updateStatus(`Nhấn lên bản đồ để chọn điểm ${mode === 'start' ? 'bắt đầu' : 'đến'}`);
}

function updateStatus(msg) {
    document.getElementById('status').innerText = msg;
}

async function findRoute() {
    const startEl = document.getElementById('start-coords');
    const endEl = document.getElementById('end-coords');

    if (!startEl.dataset.lat || !endEl.dataset.lat) {
        updateStatus("Vui lòng chọn cả điểm đi và điểm đến!");
        return;
    }

    const start = [parseFloat(startEl.dataset.lat), parseFloat(startEl.dataset.lng)];
    const end = [parseFloat(endEl.dataset.lat), parseFloat(endEl.dataset.lng)];
    const startNodeId = startEl.dataset.nodeid;
    const endNodeId = endEl.dataset.nodeid;

    const algo = document.getElementById('algorithm').value;

    updateStatus("Đang tìm đường tối ưu...");

    try {
        const payload = {
            start: start,
            end: end,
            algorithm: algo
        };

        // Add node IDs if available
        if (startNodeId) payload.startNodeId = parseInt(startNodeId);
        if (endNodeId) payload.endNodeId = parseInt(endNodeId);

        const response = await fetch('http://localhost:5000/route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (data.error) {
            updateStatus(`Lỗi: ${data.error}`);
            return;
        }

        if (routeLine) map.removeLayer(routeLine);

        // Draw path - solid line following actual road geometry
        routeLine = L.polyline(data.path, {
            color: '#3b82f6',
            weight: 5,
            opacity: 0.9,
            lineCap: 'round',
            lineJoin: 'round'
        }).addTo(map);

        // Fit bounds
        map.fitBounds(routeLine.getBounds(), { padding: [50, 50] });

        // Display stats
        const stats = data.stats;
        updateStatus(`Kết quả: ${stats.distance_km} km | ~${stats.travel_time_minutes} phút`);

    } catch (err) {
        console.error(err);
        updateStatus("Không thể kết nối đến server backend.");
    }
}
