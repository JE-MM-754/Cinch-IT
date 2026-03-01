import { Column as ColumnType } from '@/types/kanban';
import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import Task from './Task';

interface ColumnProps {
  column: ColumnType;
  onPauseTask?: (taskId: string) => void;
  onCancelTask?: (taskId: string) => void;
}

const columnColors = {
  'ideas': 'bg-blue-50 border-blue-200',
  'start-launch': 'bg-yellow-50 border-yellow-200', 
  'in-progress': 'bg-orange-50 border-orange-200',
  'complete': 'bg-green-50 border-green-200'
};

export default function Column({ column, onPauseTask, onCancelTask }: ColumnProps) {
  const { setNodeRef, isOver } = useDroppable({
    id: column.id
  });

  const columnColorClass = columnColors[column.id as keyof typeof columnColors] || 'bg-gray-50 border-gray-200';

  return (
    <div
      ref={setNodeRef}
      className={`flex flex-col w-80 h-full rounded-lg border-2 ${columnColorClass} ${
        isOver ? 'border-blue-400 bg-blue-100' : ''
      } transition-colors`}
    >
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-1">
          {column.title}
        </h2>
        <span className="text-sm text-gray-500">
          {column.tasks.length} {column.tasks.length === 1 ? 'task' : 'tasks'}
        </span>
      </div>
      
      <div
        className="flex-1 p-4 overflow-y-auto"
      >
        <SortableContext
          items={column.tasks.map(task => task.id)}
          strategy={verticalListSortingStrategy}
        >
          <div className="space-y-3">
            {column.tasks.map((task) => (
              <Task 
                key={task.id} 
                task={task} 
                columnId={column.id}
                onPause={onPauseTask}
                onCancel={onCancelTask}
              />
            ))}
          </div>
        </SortableContext>
        
        {column.tasks.length === 0 && (
          <div className="flex items-center justify-center h-32 text-gray-400">
            <p className="text-sm">Drop tasks here</p>
          </div>
        )}
      </div>
    </div>
  );
}