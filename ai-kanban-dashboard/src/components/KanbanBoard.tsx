'use client';

import { useState } from 'react';
import {
  DndContext,
  DragEndEvent,
  DragOverEvent,
  DragOverlay,
  DragStartEvent,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import { arrayMove } from '@dnd-kit/sortable';
import { Column as ColumnType, Task as TaskType } from '@/types/kanban';
import { initialColumns } from '@/data/mockTasks';
import Column from './Column';
import Task from './Task';

export default function KanbanBoard() {
  const [columns, setColumns] = useState<ColumnType[]>(initialColumns);
  const [activeTask, setActiveTask] = useState<TaskType | null>(null);

  function handlePauseTask(taskId: string) {
    setColumns(prevColumns => {
      const newColumns = [...prevColumns];
      
      // Find task in In Progress column
      const inProgressIndex = newColumns.findIndex(col => col.id === 'in-progress');
      const ideasIndex = newColumns.findIndex(col => col.id === 'ideas');
      
      if (inProgressIndex === -1 || ideasIndex === -1) return prevColumns;
      
      const task = newColumns[inProgressIndex].tasks.find(t => t.id === taskId);
      if (!task) return prevColumns;
      
      // Remove from In Progress
      newColumns[inProgressIndex] = {
        ...newColumns[inProgressIndex],
        tasks: newColumns[inProgressIndex].tasks.filter(t => t.id !== taskId)
      };
      
      // Add to Ideas
      newColumns[ideasIndex] = {
        ...newColumns[ideasIndex],
        tasks: [...newColumns[ideasIndex].tasks, task]
      };
      
      return newColumns;
    });
  }

  function handleCancelTask(taskId: string) {
    setColumns(prevColumns => {
      const newColumns = [...prevColumns];
      
      // Find and remove task from In Progress column
      const inProgressIndex = newColumns.findIndex(col => col.id === 'in-progress');
      if (inProgressIndex === -1) return prevColumns;
      
      newColumns[inProgressIndex] = {
        ...newColumns[inProgressIndex],
        tasks: newColumns[inProgressIndex].tasks.filter(t => t.id !== taskId)
      };
      
      return newColumns;
    });
  }

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  function handleDragStart(event: DragStartEvent) {
    const { active } = event;
    
    // Find the active task
    for (const column of columns) {
      const task = column.tasks.find(t => t.id === active.id);
      if (task) {
        setActiveTask(task);
        break;
      }
    }
  }

  function handleDragOver(event: DragOverEvent) {
    const { active, over } = event;
    
    if (!over) return;

    const activeId = active.id;
    const overId = over.id;

    if (activeId === overId) return;

    // Find the active and over columns
    const activeColumnIndex = columns.findIndex(col => 
      col.tasks.some(task => task.id === activeId)
    );
    
    const overColumnIndex = columns.findIndex(col => col.id === overId);

    if (activeColumnIndex === -1) return;

    // DRAG RESTRICTION: Only allow drag from "Ideas" to "Start/Launch"
    const activeColumn = columns[activeColumnIndex];
    const overColumn = overColumnIndex !== -1 ? columns[overColumnIndex] : null;
    
    if (overColumn && !(activeColumn.id === 'ideas' && overColumn.id === 'start-launch')) {
      return; // Block this drag operation - only allow Ideas → Start/Launch
    }

    // If dropping on a different column
    if (overColumnIndex !== -1 && activeColumnIndex !== overColumnIndex) {
      setColumns(prevColumns => {
        const newColumns = [...prevColumns];
        
        // Remove task from active column
        const activeTask = newColumns[activeColumnIndex].tasks.find(
          task => task.id === activeId
        );
        
        if (!activeTask) return prevColumns;
        
        newColumns[activeColumnIndex] = {
          ...newColumns[activeColumnIndex],
          tasks: newColumns[activeColumnIndex].tasks.filter(
            task => task.id !== activeId
          )
        };
        
        // Add task to over column
        newColumns[overColumnIndex] = {
          ...newColumns[overColumnIndex],
          tasks: [...newColumns[overColumnIndex].tasks, activeTask]
        };
        
        return newColumns;
      });
    }
  }

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    
    if (!over) {
      setActiveTask(null);
      return;
    }

    const activeId = active.id;
    const overId = over.id;

    if (activeId === overId) {
      setActiveTask(null);
      return;
    }

    // Find which columns contain the active and over items
    const activeColumnIndex = columns.findIndex(col => 
      col.tasks.some(task => task.id === activeId)
    );
    
    const overTaskColumnIndex = columns.findIndex(col => 
      col.tasks.some(task => task.id === overId)
    );

    // Find the target column (either column drop or task drop)
    const overColumnIndex = columns.findIndex(col => col.id === overId);
    const targetColumnIndex = overColumnIndex !== -1 ? overColumnIndex : overTaskColumnIndex;
    
    // DRAG RESTRICTION: Only allow drag from "Ideas" to "Start/Launch" 
    const activeColumn = columns[activeColumnIndex];
    const targetColumn = targetColumnIndex !== -1 ? columns[targetColumnIndex] : null;
    
    if (activeColumn && targetColumn && !(activeColumn.id === 'ideas' && targetColumn.id === 'start-launch')) {
      setActiveTask(null);
      return; // Block this drag operation - only allow Ideas → Start/Launch
    }

    // If reordering within the same column
    if (activeColumnIndex === overTaskColumnIndex && activeColumnIndex !== -1) {
      setColumns(prevColumns => {
        const newColumns = [...prevColumns];
        const column = newColumns[activeColumnIndex];
        
        const activeIndex = column.tasks.findIndex(task => task.id === activeId);
        const overIndex = column.tasks.findIndex(task => task.id === overId);
        
        if (activeIndex !== -1 && overIndex !== -1) {
          newColumns[activeColumnIndex] = {
            ...column,
            tasks: arrayMove(column.tasks, activeIndex, overIndex)
          };
        }
        
        return newColumns;
      });
    }

    setActiveTask(null);
  }

  return (
    <div className="w-full h-screen bg-gray-100">
      <div className="p-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            AI Kanban Dashboard
          </h1>
          <p className="text-gray-600">
            Manage CinchIT, MetaForge, and Job Search projects
          </p>
        </div>
        
        <DndContext
          sensors={sensors}
          onDragStart={handleDragStart}
          onDragOver={handleDragOver}
          onDragEnd={handleDragEnd}
        >
          <div className="flex gap-6 overflow-x-auto pb-6">
            {columns.map((column) => (
              <Column 
                key={column.id} 
                column={column}
                onPauseTask={handlePauseTask}
                onCancelTask={handleCancelTask}
              />
            ))}
          </div>
          
          <DragOverlay>
            {activeTask ? <Task task={activeTask} /> : null}
          </DragOverlay>
        </DndContext>
      </div>
    </div>
  );
}