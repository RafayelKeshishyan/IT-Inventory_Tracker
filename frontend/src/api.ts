import { Item, ItemCreate, ItemUpdate, DashboardStats } from './types';

// Use environment variable for API base URL
// In development: http://localhost:8000/api
// In production (Vercel): /api (same domain)
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || 'An error occurred');
  }
  return response.json();
}

export async function fetchDashboard(): Promise<DashboardStats> {
  const response = await fetch(`${API_BASE}/dashboard`);
  return handleResponse(response);
}

export async function fetchItems(params?: {
  search?: string;
  type?: string;
  status?: string;
  location?: string;
}): Promise<Item[]> {
  const searchParams = new URLSearchParams();
  if (params?.search) searchParams.set('search', params.search);
  if (params?.type) searchParams.set('type', params.type);
  if (params?.status) searchParams.set('status', params.status);
  if (params?.location) searchParams.set('location', params.location);
  
  const query = searchParams.toString();
  const response = await fetch(`${API_BASE}/items${query ? `?${query}` : ''}`);
  return handleResponse(response);
}

export async function fetchItem(id: number): Promise<Item> {
  const response = await fetch(`${API_BASE}/items/${id}`);
  return handleResponse(response);
}

export async function createItem(item: ItemCreate): Promise<Item> {
  const response = await fetch(`${API_BASE}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
  });
  return handleResponse(response);
}

export async function updateItem(id: number, item: ItemUpdate): Promise<Item> {
  const response = await fetch(`${API_BASE}/items/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
  });
  return handleResponse(response);
}

export async function deleteItem(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/items/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || 'An error occurred');
  }
}

export async function fetchLocations(): Promise<string[]> {
  const response = await fetch(`${API_BASE}/locations`);
  return handleResponse(response);
}
