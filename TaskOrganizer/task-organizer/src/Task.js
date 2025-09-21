import React from 'react';

function Task({ task, timer, sourceColumn, onToggleTimer, formatTime }) {
  const handleDragStart = (e) => {
    e.dataTransfer.setData('text/plain', JSON.stringify({
      taskId: task.id,
      sourceColumn
    }));
  };

  const handleClick = () => {
    onToggleTimer(task.id);
  };

  const isRunning = timer?.isRunning || false;
  const elapsed = timer?.elapsed || 0;

  return (
    <div
      className={`task ${isRunning ? 'running' : ''}`}
      draggable
      onDragStart={handleDragStart}
      onClick={handleClick}
    >
      <div className="task-name">{task.name}</div>
      <div className="task-timer">
        {formatTime(elapsed)}
        {isRunning && <span className="timer-indicator">●</span>}
      </div>
    </div>
  );
}

export default Task;