// Sample report data
const reports = [
    {
        id: "WB-2023-00145",
        type: "leakage",
        location: "123 Main Street, Mbeya",
        coords: [-8.9094, 33.4608],
        date: "2023-10-15T09:23:00",
        reporter: "John Doe (johndoe@email.com)",
        status: "pending",
        severity: "medium",
        description: "Large water leakage from broken pipe at street corner. Water has been flowing for over 24 hours. Street is partially flooded.",
        quality: "Brown/Dirty",
        images: [
            "https://via.placeholder.com/600x400?text=Leakage+1",
            "https://via.placeholder.com/600x400?text=Leakage+2",
            "https://via.placeholder.com/600x400?text=Leakage+3"
        ]
    },
    {
        id: "WB-2023-00146",
        type: "quality",
        location: "456 Market Road, Mbeya",
        coords: [-8.9123, 33.4587],
        date: "2023-10-15T11:45:00",
        reporter: "Jane Smith (janesmith@email.com)",
        status: "in-progress",
        severity: "high",
        description: "Brown water coming from taps with strange chemical smell. Affecting entire neighborhood.",
        quality: "Contaminated",
        images: [
            "https://via.placeholder.com/600x400?text=Quality+1",
            "https://via.placeholder.com/600x400?text=Quality+2"
        ]
    },
    {
        id: "WB-2023-00147",
        type: "leakage",
        location: "789 School Lane, Mbeya",
        coords: [-8.9078, 33.4621],
        date: "2023-10-14T16:12:00",
        reporter: "Robert Johnson (robertj@email.com)",
        status: "resolved",
        severity: "low",
        description: "Small leak from water meter. Minimal water loss.",
        quality: "Clear",
        images: [
            "https://via.placeholder.com/600x400?text=Leakage+4"
        ]
    },
    {
        id: "WB-2023-00148",
        type: "quality",
        location: "321 Hospital Avenue, Mbeya",
        coords: [-8.9056, 33.4553],
        date: "2023-10-16T08:30:00",
        reporter: "Mary Williams (maryw@email.com)",
        status: "pending",
        severity: "critical",
        description: "Water has strong sewage smell. Multiple residents reporting stomach issues after consumption.",
        quality: "Contaminated",
        images: [
            "https://via.placeholder.com/600x400?text=Quality+3",
            "https://via.placeholder.com/600x400?text=Quality+4"
        ]
    }
];

// DOM Elements
const reportsTable = document.getElementById('reports-table');
const reportFilter = document.getElementById('report-filter');
const statusFilter = document.getElementById('status-filter');
const reportDetailsModal = new bootstrap.Modal(document.getElementById('reportDetailsModal'));

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadReports();
    setupEventListeners();
});

// Load reports into the table
function loadReports(filterType = 'all', filterStatus = 'all') {
    const tbody = reportsTable.querySelector('tbody');
    tbody.innerHTML = '';

    const filteredReports = reports.filter(report => {
        const typeMatch = filterType === 'all' || report.type === filterType;
        const statusMatch = filterStatus === 'all' || report.status === filterStatus;
        return typeMatch && statusMatch;
    });

    if (filteredReports.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td colspan="7" class="text-center py-4">No reports found matching your criteria</td>`;
        tbody.appendChild(tr);
        return;
    }

    filteredReports.forEach(report => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${report.id}</td>
            <td>${report.type === 'leakage' ? 'Water Leakage' : 'Water Quality'}</td>
            <td>${report.location}</td>
            <td>${formatDate(report.date)}</td>
            <td><span class="status-badge ${report.status}">${formatStatus(report.status)}</span></td>
            <td><span class="severity-badge ${report.severity}">${formatSeverity(report.severity)}</span></td>
            <td>
                <button class="action-btn view" data-id="${report.id}">View</button>
                <button class="action-btn edit" data-id="${report.id}">Edit</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format status for display
function formatStatus(status) {
    const statusMap = {
        'pending': 'Pending',
        'in-progress': 'In Progress',
        'resolved': 'Resolved'
    };
    return statusMap[status] || status;
}

// Format severity for display
function formatSeverity(severity) {
    const severityMap = {
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
        'critical': 'Critical'
    };
    return severityMap[severity] || severity;
}

// Setup event listeners
function setupEventListeners() {
    // Filter change events
    reportFilter.addEventListener('change', function() {
        loadReports(this.value, statusFilter.value);
    });
    
    statusFilter.addEventListener('change', function() {
        loadReports(reportFilter.value, this.value);
    });

    // View report button clicks
    reportsTable.addEventListener('click', function(e) {
        if (e.target.classList.contains('view')) {
            const reportId = e.target.getAttribute('data-id');
            showReportDetails(reportId);
        }
    });

    // Thumbnail click events in modal
    document.querySelector('.thumbnail-container')?.addEventListener('click', function(e) {
        if (e.target.closest('.thumbnail')) {
            const thumbnails = document.querySelectorAll('.thumbnail');
            thumbnails.forEach(thumb => thumb.classList.remove('active'));
            e.target.closest('.thumbnail').classList.add('active');
            
            const imgSrc = e.target.closest('.thumbnail').querySelector('img').src;
            document.getElementById('report-main-image').src = imgSrc;
        }
    });
}

// Show report details in modal
function showReportDetails(reportId) {
    const report = reports.find(r => r.id === reportId);
    if (!report) return;

    // Populate modal with report data
    document.getElementById('report-id').textContent = report.id;
    document.getElementById('report-type').textContent = report.type === 'leakage' ? 'Water Leakage' : 'Water Quality';
    document.getElementById('report-date').textContent = formatDate(report.date);
    document.getElementById('report-reporter').textContent = report.reporter;
    document.getElementById('report-address').textContent = report.location;
    document.getElementById('report-coords').textContent = report.coords.join(', ');
    document.getElementById('report-description').textContent = report.description;
    document.getElementById('report-quality').textContent = report.quality;
    document.getElementById('report-severity').textContent = formatSeverity(report.severity);
    
    // Set status select
    const statusSelect = document.getElementById('status-select');
    statusSelect.value = report.status;
    
    // Set main image
    const mainImage = document.getElementById('report-main-image');
    mainImage.src = report.images[0];
    mainImage.alt = `${report.type} report image`;
    
    // Set thumbnails
    const thumbnailContainer = document.querySelector('.thumbnail-container');
    thumbnailContainer.innerHTML = '';
    
    report.images.forEach((img, index) => {
        const thumbnail = document.createElement('div');
        thumbnail.className = `thumbnail ${index === 0 ? 'active' : ''}`;
        thumbnail.innerHTML = `<img src="${img}" alt="Thumbnail ${index + 1}">`;
        thumbnailContainer.appendChild(thumbnail);
    });
    
    // Initialize map
    initMap(report.coords);
    
    // Show modal
    reportDetailsModal.show();
}

// Initialize map for report location
function initMap(coords) {
    const mapElement = document.getElementById('report-map');
    if (!mapElement) return;
    
    // In a real implementation, you would use Google Maps API
    // This is just a placeholder
    mapElement.innerHTML = `
        <div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background-color:#eee;color:#555;">
            Map View: ${coords[0]}, ${coords[1]}
        </div>
    `;
    
    // Actual Google Maps implementation would look like:
    /*
    const map = new google.maps.Map(mapElement, {
        center: { lat: coords[0], lng: coords[1] },
        zoom: 15
    });
    
    new google.maps.Marker({
        position: { lat: coords[0], lng: coords[1] },
        map: map,
        title: 'Report Location'
    });
    */
}