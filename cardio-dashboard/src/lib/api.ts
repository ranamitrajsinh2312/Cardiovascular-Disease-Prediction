const defaultApiBaseUrl = process.env.NODE_ENV === 'production'
  ? 'https://cardiovascular-prediction-api.vercel.app'
  : 'http://localhost:5000'

const apiBaseUrl = (process.env.NEXT_PUBLIC_API_URL?.trim() || defaultApiBaseUrl).replace(/\/$/, '')

export function apiUrl(path: string) {
  if (!path.startsWith('/')) {
    return `${apiBaseUrl}/${path}`
  }

  return `${apiBaseUrl}${path}`
}

export const dashboardApiUnavailableMessage = `Could not fetch model information. Ensure the API server is running at ${apiBaseUrl}`