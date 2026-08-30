let currentIncidentId = null;
let eventSource = null;

async function launchScenario(scenario) {
    // Reset UI
    document.getElementById('trace-log').innerHTML = '';
    document.getElementById('telemetry-display').innerHTML = '<div class="empty-state">Initializing simulation...</div>';
    
    // Close existing connection
    if (eventSource) {
        eventSource.close();
    }

    try {
        const response = await fetch('/api/incidents/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario })
        });
        const data = await response.json();
        currentIncidentId = data.id;
        
        startSSE();
    } catch (err) {
        console.error("Failed to launch scenario", err);
    }
}

function startSSE() {
    eventSource = new EventSource(`/api/incidents/${currentIncidentId}/stream`);

    eventSource.addEventListener('telemetry', (e) => {
        const data = JSON.parse(e.data);
        renderTelemetry(data);
    });

    eventSource.addEventListener('trace', (e) => {
        const data = JSON.parse(e.data);
        appendTrace(data);
    });

    eventSource.addEventListener('approval', (e) => {
        const data = JSON.parse(e.data);
        showApprovalDialog(data);
    });

    eventSource.addEventListener('status', (e) => {
        const data = JSON.parse(e.data);
        const trace = document.getElementById('trace-log');
        trace.innerHTML += `
            <div class="trace-item" style="border-color: ${data.status === 'resolved' ? 'var(--success)' : 'var(--danger)'}">
                <strong>Investigation Finished</strong><br/>
                Status: ${data.status.toUpperCase()}
            </div>
        `;
        eventSource.close();
    });

    eventSource.onerror = (err) => {
        console.error("SSE Error:", err);
        eventSource.close();
    };
}

function renderTelemetry(data) {
    const container = document.getElementById('telemetry-display');
    container.innerHTML = '';
    
    for (const [service, details] of Object.entries(data.services)) {
        const metrics = data.metrics[service] || {};
        const statusClass = `status-${details.status || 'down'}`;
        
        let metricsHtml = Object.entries(metrics)
            .map(([k, v]) => `<div><small>${k}:</small> <strong>${v}</strong></div>`)
            .join('');

        container.innerHTML += `
            <div class="metric-card ${statusClass}">
                <h4>${service}</h4>
                <div style="color: var(--text-secondary); margin-bottom: 0.5rem; text-transform: uppercase; font-size: 0.8rem;">
                    Status: <span style="color: var(--text-primary)">${details.status}</span>
                </div>
                ${metricsHtml}
            </div>
        `;
    }
}

function appendTrace(data) {
    const container = document.getElementById('trace-log');
    
    // Remove empty state if present
    const empty = container.querySelector('.empty-state');
    if (empty) empty.remove();

    let toolHtml = '';
    if (data.tool) {
        toolHtml = `<div style="margin-top: 0.5rem; font-family: monospace; color: var(--accent-blue);">Action: ${data.tool}</div>`;
    }

    container.innerHTML += `
        <div class="trace-item">
            <div>${data.message}</div>
            ${toolHtml}
        </div>
    `;
    container.scrollTop = container.scrollHeight;
}

function showApprovalDialog(data) {
    const dialog = document.getElementById('approval-dialog');
    const details = document.getElementById('approval-details');
    
    details.innerHTML = `
Tool: ${data.tool}
Args: ${JSON.stringify(data.args, null, 2)}
    `;
    
    dialog.classList.remove('hidden');
}

async function approveAction() {
    document.getElementById('approval-dialog').classList.add('hidden');
    appendTrace({ message: "Approving action..." });
    
    await fetch(`/api/incidents/${currentIncidentId}/approve`, {
        method: 'POST'
    });
}

function rejectAction() {
    document.getElementById('approval-dialog').classList.add('hidden');
    appendTrace({ message: "Action rejected by human." });
    if (eventSource) eventSource.close();
}
