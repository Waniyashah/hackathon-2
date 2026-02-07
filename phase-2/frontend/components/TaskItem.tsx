import React from 'react';
import { Task } from '../types';

interface TaskItemProps {
  task: Task;
  onToggle: (taskId: string, completed: boolean) => void;
  onDelete: (taskId: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete }) => {
  const handleToggle = () => {
    onToggle(task.id, !task.completed);
  };

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete task "${task.title}"?`)) {
      onDelete(task.id);
    }
  };

  return (
    <li className="px-6 py-4 hover:bg-gray-50">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            id={`task-${task.id}`}
            name={`task-${task.id}`}
            type="checkbox"
            checked={task.completed}
            onChange={handleToggle}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label
            htmlFor={`task-${task.id}`}
            className={`ml-3 block text-sm font-medium ${
              task.completed ? 'text-gray-500 line-through' : 'text-gray-700'
            }`}
          >
            {task.title}
          </label>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-xs text-gray-500">
            {new Date(task.created_at).toLocaleDateString()}
          </span>
          <button
            onClick={handleDelete}
            className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Delete
          </button>
        </div>
      </div>
      {task.description && (
        <div className="mt-2 ml-7 text-sm text-gray-500">
          {task.description}
        </div>
      )}
    </li>
  );
};

export default TaskItem;