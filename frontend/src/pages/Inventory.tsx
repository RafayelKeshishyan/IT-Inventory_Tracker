import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { fetchItems, createItem, updateItem, deleteItem } from '../api';
import { Item, ItemCreate } from '../types';
import ItemCard from '../components/ItemCard';
import ItemForm from '../components/ItemForm';
import SearchBar from '../components/SearchBar';

export default function Inventory() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Form state
  const [showForm, setShowForm] = useState(searchParams.get('showForm') === 'true');
  const [editingItem, setEditingItem] = useState<Item | null>(null);
  
  // Filter state
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [typeFilter, setTypeFilter] = useState(searchParams.get('type') || '');
  const [statusFilter, setStatusFilter] = useState(searchParams.get('status') || '');

  useEffect(() => {
    loadItems();
  }, [search, typeFilter, statusFilter]);

  useEffect(() => {
    // Update URL params when filters change
    const params = new URLSearchParams();
    if (search) params.set('search', search);
    if (typeFilter) params.set('type', typeFilter);
    if (statusFilter) params.set('status', statusFilter);
    setSearchParams(params, { replace: true });
  }, [search, typeFilter, statusFilter, setSearchParams]);

  const loadItems = async () => {
    try {
      setLoading(true);
      const data = await fetchItems({
        search: search || undefined,
        type: typeFilter || undefined,
        status: statusFilter || undefined,
      });
      setItems(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load items');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (data: ItemCreate) => {
    try {
      await createItem(data);
      setShowForm(false);
      loadItems();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create item');
    }
  };

  const handleUpdate = async (data: ItemCreate) => {
    if (!editingItem) return;
    try {
      await updateItem(editingItem.id, data);
      setEditingItem(null);
      loadItems();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update item');
    }
  };

  const handleDelete = async (item: Item) => {
    if (!confirm(`Are you sure you want to delete "${item.name}"?`)) return;
    try {
      await deleteItem(item.id);
      loadItems();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete item');
    }
  };

  const clearFilters = () => {
    setSearch('');
    setTypeFilter('');
    setStatusFilter('');
  };

  const hasFilters = search || typeFilter || statusFilter;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-2xl font-bold text-gray-900">Inventory</h2>
        <button
          onClick={() => setShowForm(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Item
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <SearchBar
              value={search}
              onChange={setSearch}
              placeholder="Search by name, location, or notes..."
            />
          </div>
          <div className="flex gap-3">
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="device">Devices</option>
              <option value="part">Parts</option>
            </select>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Status</option>
              <option value="available">Available</option>
              <option value="in_use">In Use</option>
              <option value="checked_out">Checked Out</option>
              <option value="broken">Broken</option>
            </select>
            {hasFilters && (
              <button
                onClick={clearFilters}
                className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900"
              >
                Clear
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Results count */}
      <div className="text-sm text-gray-500">
        {loading ? 'Loading...' : `${items.length} item${items.length !== 1 ? 's' : ''} found`}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      )}

      {/* Items Grid */}
      {!loading && !error && (
        <>
          {items.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No items found</h3>
              <p className="mt-1 text-sm text-gray-500">
                {hasFilters ? 'Try adjusting your filters.' : 'Get started by adding your first item.'}
              </p>
              {!hasFilters && (
                <button
                  onClick={() => setShowForm(true)}
                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm"
                >
                  Add Item
                </button>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {items.map((item) => (
                <ItemCard
                  key={item.id}
                  item={item}
                  onEdit={setEditingItem}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          )}
        </>
      )}

      {/* Loading state */}
      {loading && (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* Form Modal */}
      {(showForm || editingItem) && (
        <ItemForm
          item={editingItem}
          onSubmit={editingItem ? handleUpdate : handleCreate}
          onCancel={() => {
            setShowForm(false);
            setEditingItem(null);
          }}
        />
      )}
    </div>
  );
}
