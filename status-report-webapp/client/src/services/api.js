const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`);

  if (!response.ok) {
    const content = await response.json().catch(() => ({}));
    throw new Error(content.message || 'Request failed');
  }

  return response.json();
}

export function fetchCurrentReport() {
  return fetchJson('/api/reports/current');
}
