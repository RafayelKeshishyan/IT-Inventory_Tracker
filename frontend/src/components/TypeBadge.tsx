import { ItemType } from '../types';

interface TypeBadgeProps {
  type: ItemType;
}

const typeConfig: Record<ItemType, { label: string; className: string }> = {
  device: {
    label: 'Device',
    className: 'bg-purple-100 text-purple-800',
  },
  part: {
    label: 'Part',
    className: 'bg-gray-100 text-gray-800',
  },
};

export default function TypeBadge({ type }: TypeBadgeProps) {
  const config = typeConfig[type];
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.className}`}>
      {config.label}
    </span>
  );
}
