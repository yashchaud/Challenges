import React, { useState, useEffect } from 'react';
import TaskColumn from './TaskColumn';
import './App.css';

function App() {
  const [tasks, setTasks] = useState(() => {
    const saved = localStorage.getItem('tasks');
    return saved ? JSON.parse(saved) : {
      todo: [],
      inProgress: [],
      done: []
    };
  });

  const [timers, setTimers] = useState(() => {
    const saved = localStorage.getItem('timers');
    return saved ? JSON.parse(saved) : {};
  });

  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }, [tasks]);

  useEffect(() => {
    localStorage.setItem('timers', JSON.stringify(timers));
  }, [timers]);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimers(prev => {
        const updated = {};
        Object.keys(prev).forEach(taskId => {
          updated[taskId] = {
            ...prev[taskId],
            elapsed: prev[taskId].isRunning ? prev[taskId].elapsed + 1 : prev[taskId].elapsed
          };
        });
        return updated;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const addTask = (columnId, taskName) => {
    const newTask = {
      id: Date.now().toString(),
      name: taskName
    };

    setTasks(prev => ({
      ...prev,
      [columnId]: [...prev[columnId], newTask]
    }));

    setTimers(prev => ({
      ...prev,
      [newTask.id]: { elapsed: 0, isRunning: false }
    }));
  };

  const toggleTimer = (taskId) => {
    setTimers(prev => ({
      ...prev,
      [taskId]: {
        ...prev[taskId],
        isRunning: !prev[taskId]?.isRunning
      }
    }));
  };

  const moveTask = (taskId, sourceColumn, targetColumn) => {
    const sourceIndex = tasks[sourceColumn].findIndex(task => task.id === taskId);
    const taskToMove = tasks[sourceColumn][sourceIndex];

    setTasks(prev => ({
      ...prev,
      [sourceColumn]: prev[sourceColumn].filter(task => task.id !== taskId),
      [targetColumn]: [...prev[targetColumn], taskToMove]
    }));
  };

  return (
    <div className="app">
      <div className="board">
        <TaskColumn
          id="todo"
          title="To Do"
          tasks={tasks.todo}
          timers={timers}
          onAddTask={addTask}
          onToggleTimer={toggleTimer}
          onMoveTask={moveTask}
        />
        <TaskColumn
          id="inProgress"
          title="In Progress"
          tasks={tasks.inProgress}
          timers={timers}
          onAddTask={addTask}
          onToggleTimer={toggleTimer}
          onMoveTask={moveTask}
        />
        <TaskColumn
          id="done"
          title="Done"
          tasks={tasks.done}
          timers={timers}
          onAddTask={addTask}
          onToggleTimer={toggleTimer}
          onMoveTask={moveTask}
        />
      </div>
    </div>
  );
}

export default App;