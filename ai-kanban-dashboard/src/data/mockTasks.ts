import { Task, Column } from '@/types/kanban';

export const mockTasks: Task[] = [
  // CinchIT tasks
  {
    id: 'cinch-1',
    title: 'MVP Product Definition',
    description: 'Define core features for CinchIT MVP',
    project: 'CinchIT',
    priority: 'high',
    tags: ['strategy', 'product']
  },
  {
    id: 'cinch-2', 
    title: 'User Research & Validation',
    description: 'Conduct user interviews for CinchIT pain points',
    project: 'CinchIT',
    priority: 'high',
    tags: ['research', 'validation']
  },
  {
    id: 'cinch-3',
    title: 'Landing Page Development',
    description: 'Build marketing landing page with waitlist',
    project: 'CinchIT',
    priority: 'medium',
    tags: ['development', 'marketing']
  },
  {
    id: 'cinch-4',
    title: 'Beta Testing Program',
    description: 'Launch closed beta with initial users',
    project: 'CinchIT',
    priority: 'medium',
    tags: ['testing', 'beta']
  },

  // MetaForge tasks
  {
    id: 'meta-1',
    title: 'AI Agent Architecture',
    description: 'Design multi-agent system architecture',
    project: 'MetaForge', 
    priority: 'high',
    tags: ['ai', 'architecture']
  },
  {
    id: 'meta-2',
    title: 'LLM Integration Pipeline',
    description: 'Build pipeline for LLM model integration',
    project: 'MetaForge',
    priority: 'high',
    tags: ['ai', 'development']
  },
  {
    id: 'meta-3',
    title: 'Enterprise Sales Deck',
    description: 'Create compelling B2B sales presentation',
    project: 'MetaForge',
    priority: 'medium',
    tags: ['sales', 'enterprise']
  },
  {
    id: 'meta-4',
    title: 'Demo Environment Setup',
    description: 'Build sandbox demo for prospects',
    project: 'MetaForge',
    priority: 'low',
    tags: ['demo', 'sales']
  },

  // Job Search tasks
  {
    id: 'job-1',
    title: 'Target Company Research',
    description: 'Research top 50 target companies for VP Sales roles',
    project: 'Job Search',
    priority: 'high',
    tags: ['research', 'networking']
  },
  {
    id: 'job-2',
    title: 'LinkedIn Profile Optimization',
    description: 'Update LinkedIn with recent achievements',
    project: 'Job Search',
    priority: 'medium',
    tags: ['linkedin', 'branding']
  },
  {
    id: 'job-3',
    title: 'Interview Preparation',
    description: 'Prepare MEDDPICC case studies and success stories',
    project: 'Job Search',
    priority: 'high',
    tags: ['interviews', 'preparation']
  },
  {
    id: 'job-4',
    title: 'Salary Negotiation Research',
    description: 'Research market rates for $400k+ OTE roles',
    project: 'Job Search',
    priority: 'low',
    tags: ['negotiation', 'research']
  },
  {
    id: 'job-5',
    title: 'Follow-up Email Templates',
    description: 'Create templates for post-interview follow-ups',
    project: 'Job Search',
    priority: 'low',
    tags: ['templates', 'communication']
  }
];

export const initialColumns: Column[] = [
  {
    id: 'ideas',
    title: 'Ideas',
    tasks: mockTasks.filter(task => ['cinch-1', 'meta-1', 'job-1'].includes(task.id))
  },
  {
    id: 'start-launch',
    title: 'Start/Launch',
    tasks: mockTasks.filter(task => ['cinch-2', 'meta-2', 'job-2', 'job-3'].includes(task.id))
  },
  {
    id: 'in-progress', 
    title: 'In Progress',
    tasks: mockTasks.filter(task => ['cinch-3', 'meta-3'].includes(task.id))
  },
  {
    id: 'complete',
    title: 'Complete',
    tasks: mockTasks.filter(task => ['cinch-4', 'meta-4', 'job-4', 'job-5'].includes(task.id))
  }
];