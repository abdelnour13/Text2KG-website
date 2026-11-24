const BASE = '/api' // ?? '/api'

// ── Helpers ───────────────────────────────────────────────────────────────────

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(body.detail ?? `HTTP ${res.status}`)
  }
  return res.json() as Promise<T>
}

// ── Graph endpoints ───────────────────────────────────────────────────────────

/** GET /graphs — list all expertise maps */
export async function listGraphs(): Promise<App.GraphSummary[]> {
  return request<App.GraphSummary[]>('/graphs')
}

/** GET /graphs/{id} — full detail for one expertise map */
export async function getGraph(id: string): Promise<App.GraphDetail> {
  return request<App.GraphDetail>(`/graphs/${encodeURIComponent(id)}`)
}

/**
 * GET /graphs/{id}/download — stream the subgraph JSON as a file download.
 * Triggers a browser download directly; returns void.
 */
export async function downloadGraph(id: string): Promise<void> {
  const res = await fetch(`${BASE}/graphs/${encodeURIComponent(id)}/download`)
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(body.detail ?? `HTTP ${res.status}`)
  }
  const blob = await res.blob()
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href     = url
  a.download = `graph_${id}.json`
  a.click()
  URL.revokeObjectURL(url)
}

// ── Visualisation endpoints ───────────────────────────────────────────────────

/** POST /graphs/{id}/vis/taxonomy */
export async function visTaxonomy(id: string): Promise<App.VisualisationResponse> {
  return request<App.VisualisationResponse>(`/graphs/${encodeURIComponent(id)}/vis/taxonomy`, {
    method: 'POST',
  })
}

/** POST /graphs/{id}/vis/expertises — optional domain/subdomain/lab filters as query params */
export async function visExpertises(
  id: string,
  filters?: { domains?: string[]; subdomains?: string[]; labs?: string[] }
): Promise<App.VisualisationResponse> {
  const qs = new URLSearchParams()
  filters?.domains?.forEach((d) => qs.append('domains', d))
  filters?.subdomains?.forEach((s) => qs.append('subdomains', s))
  filters?.labs?.forEach((l) => qs.append('labs', l))
  const query = qs.toString() ? `?${qs.toString()}` : ''
  return request<App.VisualisationResponse>(
    `/graphs/${encodeURIComponent(id)}/vis/expertises${query}`,
    { method: 'POST' }
  )
}

/** POST /graphs/{id}/vis/expertises/{community_id} */
export async function visExpertiseDetail(
  id: string,
  communityId: string
): Promise<App.VisualisationResponse> {
  return request<App.VisualisationResponse>(
    `/graphs/${encodeURIComponent(id)}/vis/expertises/${encodeURIComponent(communityId)}`,
    { method: 'POST' }
  )
}

/** POST /graphs/{id}/vis/summary */
export async function visSummary(id: string): Promise<App.VisualisationResponse> {
  return request<App.VisualisationResponse>(`/graphs/${encodeURIComponent(id)}/vis/summary`, {
    method: 'POST',
  })
}

export function downloadURL(filename : string) : string {
  return `${BASE}/download/${filename}`
}