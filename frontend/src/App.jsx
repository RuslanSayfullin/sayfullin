import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

// Автоматическое определение API URL
const API_BASE = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000/api'
  : '/api'

function App() {
  const [tasks, setTasks] = useState([])
  const [newTask, setNewTask] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchTasks()
  }, [])

  const fetchTasks = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_BASE}/tasks`)
      setTasks(response.data)
      setError('')
    } catch (error) {
      console.error('Error fetching tasks:', error)
      setError('Failed to load tasks. Please check if backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const addTask = async (e) => {
    e.preventDefault()
    if (!newTask.trim()) return

    try {
      const task = {
        title: newTask,
        completed: false
      }
      const response = await axios.post(`${API_BASE}/tasks`, task)
      setTasks([...tasks, response.data])
      setNewTask('')
      setError('')
    } catch (error) {
      console.error('Error adding task:', error)
      setError('Failed to add task. Please try again.')
    }
  }

  const toggleTask = async (task) => {
    try {
      const updatedTask = {
        title: task.title,
        completed: !task.completed
      }
      const response = await axios.put(`${API_BASE}/tasks/${task.id}`, updatedTask)
      setTasks(tasks.map(t => t.id === task.id ? response.data : t))
      setError('')
    } catch (error) {
      console.error('Error updating task:', error)
      setError('Failed to update task. Please try again.')
    }
  }

  const deleteTask = async (taskId) => {
    try {
      await axios.delete(`${API_BASE}/tasks/${taskId}`)
      setTasks(tasks.filter(t => t.id !== taskId))
      setError('')
    } catch (error) {
      console.error('Error deleting task:', error)
      setError('Failed to delete task. Please try again.')
    }
  }

  return (
    <div className="app">
      <h1>🚀 Todo Application</h1>
      <p>React + FastAPI on Remote Server</p>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={addTask} className="task-form">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Enter new task..."
          className="task-input"
          disabled={loading}
        />
        <button type="submit" className="add-button" disabled={loading}>
          {loading ? 'Adding...' : 'Add Task'}
        </button>
      </form>

      {loading ? (
        <div className="loading">Loading tasks...</div>
      ) : (
        <div className="tasks-list">
          {tasks.map(task => (
            <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
              <span 
                className="task-text"
                onClick={() => toggleTask(task)}
              >
                {task.title}
              </span>
              <button 
                onClick={() => deleteTask(task.id)}
                className="delete-button"
                disabled={loading}
              >
                Delete
              </button>
            </div>
          ))}
          {tasks.length === 0 && !loading && (
            <div className="no-tasks">No tasks yet. Add your first task above!</div>
          )}
        </div>
      )}
    </div>
  )
}

export default App