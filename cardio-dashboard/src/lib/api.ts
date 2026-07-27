const apiBaseUrl = (process.env.NEXT_PUBLIC_API_URL?.trim() || '').replace(/\/$/, '')

export function apiUrl(path: string) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`

  if (!apiBaseUrl) {
    return normalizedPath
  }

  if (!path.startsWith('/')) {
    return `${apiBaseUrl}/${path}`
  }

  return `${apiBaseUrl}${normalizedPath}`
}

export const dashboardApiUnavailableMessage = apiBaseUrl
  ? `Could not fetch model information. Ensure the API server is running at ${apiBaseUrl}`
  : 'Could not fetch model information. Ensure the in-project API routes are deployed.'