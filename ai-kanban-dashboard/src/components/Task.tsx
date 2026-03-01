import { Task as TaskType } from '@/types/kanban';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

interface TaskProps {
  task: TaskType;
  columnId?: string;
  onPause?: (taskId: string) => void;
  onCancel?: (taskId: string) => void;
}

const projectColors = {
  'CinchIT': 'bg-blue-50 border-blue-200 text-blue-800',
  'MetaForge': 'bg-green-50 border-green-200 text-green-800',
  'Job Search': 'bg-purple-50 border-purple-200 text-purple-800'
};

const priorityColors = {
  'low': 'bg-gray-100 text-gray-600',
  'medium': 'bg-yellow-100 text-yellow-800',
  'high': 'bg-red-100 text-red-800'
};

export default function Task({ task, columnId, onPause, onCancel }: TaskProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging
  } = useSortable({ id: task.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 cursor-grab hover:shadow-md transition-shadow"
    >
      <div className="flex items-start justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-900 leading-tight">
          {task.title}
        </h3>
        <span
          className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
            priorityColors[task.priority]
          }`}
        >
          {task.priority}
        </span>
      </div>
      
      {task.description && (
        <p className="text-xs text-gray-600 mb-3 line-clamp-2">
          {task.description}
        </p>
      )}
      
      <div className="flex items-center justify-between">
        <span
          className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium border ${
            projectColors[task.project]
          }`}
        >
          {task.project}
        </span>
        
        {task.tags && task.tags.length > 0 && (
          <div className="flex gap-1">
            {task.tags.slice(0, 2).map((tag, index) => (
              <span
                key={index}
                className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700"
              >
                {tag}
              </span>
            ))}
            {task.tags.length > 2 && (
              <span className="text-xs text-gray-500">+{task.tags.length - 2}</span>
            )}
          </div>
        )}
      </div>
      
      {/* Task Controls for In Progress Column */}
      {columnId === 'in-progress' && (onPause || onCancel) && (
        <div className="mt-3 pt-3 border-t border-gray-100 flex gap-2">
          {onPause && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onPause(task.id);
              }}
              className="flex-1 px-3 py-1.5 text-xs font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-md transition-colors"
            >
              ⏸️ Pause
            </button>
          )}
          {onCancel && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onCancel(task.id);
              }}
              className="flex-1 px-3 py-1.5 text-xs font-medium text-red-700 bg-red-50 hover:bg-red-100 border border-red-200 rounded-md transition-colors"
            >
              ❌ Cancel
            </button>
          )}
        </div>
      )}
    </div>
  );
}