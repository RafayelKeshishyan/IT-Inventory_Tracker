export type ItemType = 'device' | 'part';
export type ItemStatus = 'available' | 'in_use' | 'broken' | 'checked_out';

export interface Item {
  id: number;
  name: string;
  type: ItemType;
  location: string | null;
  status: ItemStatus;
  quantity: number;
  low_stock_threshold: number;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface ItemCreate {
  name: string;
  type: ItemType;
  location?: string;
  status: ItemStatus;
  quantity: number;
  low_stock_threshold: number;
  notes?: string;
}

export interface ItemUpdate {
  name?: string;
  type?: ItemType;
  location?: string;
  status?: ItemStatus;
  quantity?: number;
  low_stock_threshold?: number;
  notes?: string;
}

export interface DashboardStats {
  total_items: number;
  total_devices: number;
  total_parts: number;
  available_count: number;
  in_use_count: number;
  broken_count: number;
  checked_out_count: number;
  low_stock_items: Item[];
}
