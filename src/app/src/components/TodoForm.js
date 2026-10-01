import { useState } from 'react';

export function TodoForm({ onSubmit, isSubmitting }) {
  const [description, setDescription] = useState('');
  const [validationError, setValidationError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    const trimmed = description.trim();
    if (!trimmed) {
      setValidationError('Please enter a todo description.');
      return;
    }

    setValidationError('');
    const success = await onSubmit(trimmed);
    if (success) {
      setDescription('');
    }
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <label htmlFor="todo">ToDo:</label>
        <input
          id="todo"
          type="text"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="What needs to be done?"
          disabled={isSubmitting}
          maxLength={500}
        />
      </div>

      {validationError && (
        <p className="error-text" role="alert">{validationError}</p>
      )}

      <div className="form-actions">
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Adding...' : 'Add ToDo!'}
        </button>
      </div>
    </form>
  );
}
