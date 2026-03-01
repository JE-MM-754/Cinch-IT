export interface Task {
  id: string;
  title: string;
  description?: string;
  project: 'CinchIT' | 'MetaForge' | 'Job Search';
  priority: 'low' | 'medium' | 'high';
  tags?: string[];
  cancelled?: boolean;
}

export interface Column {
  id: string;
  title: string;
  tasks: Task[];
}

export type ColumnId = 'ideas' | 'start-launch' | 'in-progress' | 'complete';