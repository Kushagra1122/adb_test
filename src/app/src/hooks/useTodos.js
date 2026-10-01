import { useCallback, useEffect, useState } from 'react';
import { createTodo, fetchTodos } from '../api/todos';

export function useTodos() {
  const [todos, setTodos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const loadTodos = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await fetchTodos();
      setTodos(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Failed to load todos');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  const addTodo = useCallback(async (description) => {
    setIsSubmitting(true);
    setError(null);

    try {
      await createTodo(description);
      await loadTodos();
      return true;
    } catch (err) {
      setError(err.message || 'Failed to create todo');
      return false;
    } finally {
      setIsSubmitting(false);
    }
  }, [loadTodos]);

  return {
    todos,
    isLoading,
    isSubmitting,
    error,
    addTodo,
    refresh: loadTodos,
  };
}
