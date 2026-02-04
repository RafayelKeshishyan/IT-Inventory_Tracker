import { Item } from '../types';
import StatusBadge from './StatusBadge';
import TypeBadge from './TypeBadge';

interface ItemCardProps {
  item: Item;
  onEdit: (item: Item) => void;
  onDelete: (item: Item) => void;
}

export default function ItemCard({ item, onEdit, onDelete }: ItemCardProps) {
  const isLowStock = item.type === 'part' && item.quantity <= item.low_stock_threshold;

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-4 hover:shadow-md transition-shadow ${isLowStock ? 'border-orange-300 bg-orange-50' : 'border-gray-200'}`}>
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 text-lg">{item.name}</h3>
          {item.location && (
            <p className="text-sm text-gray-500 flex items-center gap-1 mt-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {item.location}
            </p>
          )}
        </div>
        <div className="flex gap-2">
          <TypeBadge type={item.type} />
          <StatusBadge status={item.status} />
        </div>
      </div>

      {item.type === 'part' && (
        <div className={`text-sm mb-3 ${isLowStock ? 'text-orange-700 font-medium' : 'text-gray-600'}`}>
          {isLowStock && (
            <span className="inline-flex items-center gap-1 mr-2">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              Low Stock!
            </span>
          )}
          Quantity: {item.quantity} (threshold: {item.low_stock_threshold})
        </div>
      )}

      {item.notes && (
        <p className="text-sm text-gray-500 mb-3 line-clamp-2">{item.notes}</p>
      )}

      <div className="flex justify-between items-center pt-3 border-t border-gray-100">
        <span className="text-xs text-gray-400">
          Updated {new Date(item.updated_at).toLocaleDateString()}
        </span>
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(item)}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(item)}
            className="text-sm text-red-600 hover:text-red-800 font-medium"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
