const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(method, path, body = null) {
  const token = localStorage.getItem('api_token')
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const options = { method, headers }
  if (body !== null) options.body = JSON.stringify(body)

  const response = await fetch(`${BASE_URL}${path}`, options)

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw { status: response.status, message: err.detail || 'Request failed' }
  }

  // 204/empty bodies: guard against JSON parse errors
  const text = await response.text()
  return text ? JSON.parse(text) : null
}

export const api = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),
  patch: (path, body) => request('PATCH', path, body)
}
