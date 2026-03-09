const apiBaseUrl = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000').replace(/\/$/, '')

export function apiUrl(path: string) {
  if (!path.startsWith('/')) {
    return `${apiBaseUrl}/${path}`
  }

  return `${apiBaseUrl}${path}`
}

export const dashboardApiUnavailableMessage = `Could not fetch model information. Ensure the API server is running at ${apiBaseUrl}`