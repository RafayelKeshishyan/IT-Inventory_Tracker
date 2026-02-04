import { ItemStatus } from '../types';

interface StatusBadgeProps {
  status: ItemStatus;
}

const statusConfig: Record<ItemStatus, { label: string; className: string }> = {
  available: {
    label: 'Available',
    className: 'bg-green-100 text-green-800',
  },
  in_use: {
    label: 'In Use',
    className: 'bg-blue-100 text-blue-800',
  },
  broken: {
    label: 'Broken',
    className: 'bg-red-100 text-red-800',
  },
  checked_out: {
    label: 'Checked Out',
    className: 'bg-yellow-100 text-yellow-800',
  },
};

export default function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.className}`}>
      {config.label}
    </span>
  );
}
