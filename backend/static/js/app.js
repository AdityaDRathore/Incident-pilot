// Application State
const AppState = {
    currentIncidentId: null,
    eventSource: null,
    incidents: [],
    evidence: [],
    hypotheses: [],
    auditLogs: []
};

// Navigation
function switchView(viewName) {
    document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));
    document.querySelectorAll('.nav-links li').forEach(l => l.classList.remove('active'));
    
    const view = document.getElementById(`view-${viewName}`);
    if (view) view.classList.remove('hidden');
    
    const navItem = document.querySelector(`.nav-links li[data-view="${viewName}"]`);
    if (navItem) navItem.classList.add('active');

    const titles = {
        'dashboard': 'Engineering Dashboard',
        'incidents': 'Active Incidents',
        'incident-detail': `Incident ${AppState.currentIncidentId ? AppState.currentIncidentId.split('-')[0] : 'Detail'}`,
        'evaluation': 'Agent Evaluation'
    };
    
    document.getElementById('page-title').textContent = titles[viewName] || 'Dashboard';
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-pane').forEach(t => t.classList.add('hidden'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    const tab = document.getElementById(`tab-${tabName}`);
    if (tab) tab.classList.remove('hidden');
    
    const btn = document.querySelector(`.tab-btn[onclick="switchTab('${tabName}')"]`);
    if (btn) btn.classList.add('active');
}

// API and SSE Connection
async function launchScenario(scenario) {
    // Reset UI State
    resetIncidentUI();
    
    try {
        const response = await fetch('/api/incidents/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario })
        });
        
        const data = await response.json();
        AppState.currentIncidentId = data.id;
        AppState.incidents.push({ id: data.id, scenario, status: data.status, timestamp: new Date().toISOString() });
        
        // Update UI
        updateIncidentList();
        setupIncidentDetailView(data.id, scenario);
        switchView('incident-detail');
        
        // Start streaming events
        startSSE(data.id);
    } catch (err) {
        console.error("Failed to launch scenario", err);
        alert("Failed to launch scenario. Is the backend running?");
    }
}

function resetIncidentUI() {
    document.getElementById('trace-log').innerHTML = '';
    document.getElementById('telemetry-display').innerHTML = '<div class="empty-state">Initializing simulation...</div>';
    document.getElementById('evidence-list').innerHTML = '<div class="empty-state">No evidence collected yet.</div>';
    document.getElementById('hypothesis-list').innerHTML = '<div class="empty-state">No hypotheses generated.</div>';
    document.getElementById('audit-log').innerHTML = '<div class="empty-state">No actions audited.</div>';
    
    AppState.evidence = [];
    AppState.hypotheses = [];
    AppState.auditLogs = [];
    
    if (AppState.eventSource) {
        AppState.eventSource.close();
    }
}

function updateIncidentList() {
    const list = document.getElementById('incident-list');
    if (AppState.incidents.length === 0) return;
    
    list.innerHTML = AppState.incidents.map(inc => `
        <div class="list-item" style="flex-direction: row; justify-content: space-between; align-items: center; cursor: pointer;" onclick="openIncident('${inc.id}')">
            <div>
                <h4>${inc.scenario}</h4>
                <small class="text-secondary">${inc.id}</small>
            </div>
            <span class="status-badge ${inc.status}">${inc.status}</span>
        </div>
    `).join('');
}

function openIncident(id) {
    const inc = AppState.incidents.find(i => i.id === id);
    if (!inc) return;
    AppState.currentIncidentId = id;
    setupIncidentDetailView(id, inc.scenario);
    switchView('incident-detail');
}

function setupIncidentDetailView(id, scenario) {
    document.getElementById('detail-incident-id').textContent = `INC-${id.split('-')[0].toUpperCase()}`;
    document.getElementById('detail-incident-desc').textContent = `Scenario: ${scenario}`;
    updateIncidentStatusBadge('investigating');
}

function updateIncidentStatusBadge(status) {
    const badge = document.getElementById('detail-incident-status');
    badge.textContent = status;
    badge.className = `status-badge ${status}`;
}

// SSE Handling
function startSSE(incidentId) {
    const eventSource = new EventSource(`/api/incidents/${incidentId}/stream`);
    AppState.eventSource = eventSource;

    eventSource.addEventListener('telemetry', (e) => {
        const data = JSON.parse(e.data);
        renderTelemetry(data);
    });

    eventSource.addEventListener('trace', (e) => {
        const data = JSON.parse(e.data);
        appendTrace(data);
        logAudit({ action: 'Agent Action', details: data.message, timestamp: new Date().toISOString() });
    });

    eventSource.addEventListener('evidence.created', (e) => {
        const data = JSON.parse(e.data);
        AppState.evidence.push(data);
        renderEvidence();
    });

    eventSource.addEventListener('hypothesis.updated', (e) => {
        const data = JSON.parse(e.data);
        AppState.hypotheses.push(data);
        renderHypotheses();
    });

    eventSource.addEventListener('approval', (e) => {
        const data = JSON.parse(e.data);
        showApprovalDialog(data);
    });

    eventSource.addEventListener('status', (e) => {
        const data = JSON.parse(e.data);
        updateIncidentStatusBadge(data.status);
        
        appendTrace({ 
            message: `Investigation Finished: ${data.status.toUpperCase()}`,
            type: data.status === 'resolved' ? 'success' : 'error'
        });
        
        // Generate Report on finish
        document.getElementById('final-report').innerHTML = `
            <h4>Executive Summary</h4>
            <p>Incident resolved via automated agent remediation.</p>
            <h4>Timeline</h4>
            <p>Total time to resolve: ~4s</p>
        `;
        
        eventSource.close();
    });

    eventSource.onerror = (err) => {
        console.error("SSE Error:", err);
        eventSource.close();
    };
}

// Rendering Data
function renderTelemetry(data) {
    const container = document.getElementById('telemetry-display');
    container.innerHTML = '';
    
    for (const [service, details] of Object.entries(data.services)) {
        const metrics = data.metrics[service] || {};
        const statusClass = `status-${details.status || 'down'}`;
        
        let metricsHtml = Object.entries(metrics)
            .map(([k, v]) => `
                <div class="metric-row">
                    <span>${k}</span>
                    <strong>${v}</strong>
                </div>
            `).join('');

        container.innerHTML += `
            <div class="metric-card ${statusClass}">
                <h4>${service}</h4>
                <div class="metric-status">${details.status}</div>
                ${metricsHtml}
            </div>
        `;
    }
}

function appendTrace(data) {
    const container = document.getElementById('trace-log');
    const empty = container.querySelector('.empty-state');
    if (empty) empty.remove();

    const typeClass = data.type || (data.tool ? 'action' : 'system');
    let toolHtml = '';
    
    if (data.tool) {
        toolHtml = `
            <div class="trace-tool">
                > Executing: ${data.tool}()<br/>
                ${data.args ? '> Args: ' + JSON.stringify(data.args) : ''}
            </div>
        `;
    }

    const time = new Date().toLocaleTimeString();
    
    container.innerHTML += `
        <div class="trace-item ${typeClass}">
            <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.25rem;">${time}</div>
            <div>${data.message}</div>
            ${toolHtml}
        </div>
    `;
    container.scrollTop = container.scrollHeight;
}

function renderEvidence() {
    const container = document.getElementById('evidence-list');
    container.innerHTML = AppState.evidence.map(e => `
        <div class="list-item">
            <h4>Evidence: ${e.evidence_id || 'System Data'}</h4>
            <p class="text-secondary">${e.content || e.details}</p>
        </div>
    `).join('');
}

function renderHypotheses() {
    const container = document.getElementById('hypothesis-list');
    container.innerHTML = AppState.hypotheses.map(h => `
        <div class="list-item">
            <h4>Hypothesis</h4>
            <p class="text-secondary">Status: ${h.status}</p>
            <p>${h.details}</p>
        </div>
    `).join('');
}

function logAudit(entry) {
    AppState.auditLogs.push(entry);
    const container = document.getElementById('audit-log');
    if (container.querySelector('.empty-state')) container.innerHTML = '';
    
    container.innerHTML += `
        <div class="list-item">
            <small class="text-secondary">${new Date(entry.timestamp).toLocaleTimeString()}</small>
            <div><strong>${entry.action}</strong>: ${entry.details}</div>
        </div>
    `;
}

// Approval Actions
function showApprovalDialog(data) {
    const dialog = document.getElementById('approval-dialog');
    const details = document.getElementById('approval-details');
    const impact = document.getElementById('approval-impact-text');
    
    details.innerHTML = `Tool: ${data.tool}\nArgs: ${JSON.stringify(data.args, null, 2)}`;
    
    if (data.tool === 'rollback_deployment') {
        impact.textContent = "Will modify production traffic routing and revert application state.";
    } else {
        impact.textContent = "Will restart a production service. Temporary latency expected.";
    }
    
    dialog.classList.remove('hidden');
    logAudit({ action: 'Approval Requested', details: `Tool: ${data.tool}`, timestamp: new Date().toISOString() });
}

async function approveAction() {
    document.getElementById('approval-dialog').classList.add('hidden');
    appendTrace({ message: "Operator approved action.", type: "success" });
    logAudit({ action: 'Approval Granted', details: `Operator granted execution.`, timestamp: new Date().toISOString() });
    
    await fetch(`/api/incidents/${AppState.currentIncidentId}/approve`, {
        method: 'POST'
    });
}

function rejectAction() {
    document.getElementById('approval-dialog').classList.add('hidden');
    appendTrace({ message: "Action rejected by operator. Investigation halted.", type: "error" });
    updateIncidentStatusBadge('failed');
    logAudit({ action: 'Approval Rejected', details: `Operator denied execution.`, timestamp: new Date().toISOString() });
    
    if (AppState.eventSource) AppState.eventSource.close();
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    switchView('dashboard');
});
