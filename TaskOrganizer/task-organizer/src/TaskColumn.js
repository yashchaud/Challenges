import React, { useState } from 'react';
import Task from './Task';

function TaskColumn({ id, title, tasks, timers, onAddTask, onToggleTimer, onMoveTask }) {
  const [isCreating, setIsCreating] = useState(false);
  const [newTaskName, setNewTaskName] = useState('');

  const handleAddClick = () => {
    setIsCreating(true);
    setNewTaskName('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (newTaskName.trim()) {
      onAddTask(id, newTaskName.trim());
      setNewTaskName('');
      setIsCreating(false);
    }
  };

  const handleCancel = () => {
    setIsCreating(false);
    setNewTaskName('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      handleCancel();
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const taskData = JSON.parse(e.dataTransfer.getData('text/plain'));
    if (taskData.sourceColumn !== id) {
      onMoveTask(taskData.taskId, taskData.sourceColumn, id);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="column" onDragOver={handleDragOver} onDrop={handleDrop}>
      <h3 className="column-title">{title}</h3>

      <div className="task-list">
        <div className="add-task-container">
          <button className="add-button" onClick={handleAddClick}>+</button>
          {isCreating && (
            <form onSubmit={handleSubmit} className="new-task-form">
              <input
                type="text"
                value={newTaskName}
                onChange={(e) => setNewTaskName(e.target.value)}
                onKeyDown={handleKeyDown}
                onBlur={handleCancel}
                placeholder="Enter task name..."
                className="new-task-input"
                autoFocus
              />
            </form>
          )}
        </div>

        {tasks.map(task => (
          <Task
            key={task.id}
            task={task}
            timer={timers[task.id]}
            sourceColumn={id}
            onToggleTimer={onToggleTimer}
            formatTime={formatTime}
          />
        ))}
      </div>
    </div>
  );
}

export default TaskColumn;