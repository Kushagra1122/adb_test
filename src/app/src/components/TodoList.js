export function TodoList({ todos, isLoading }) {
  if (isLoading) {
    return <p className="status-text">Loading todos...</p>;
  }

  if (!todos.length) {
    return <p className="status-text">No todos yet. Add your first one!</p>;
  }

  return (
    <ul className="todo-list">
      {todos.map((todo) => (
        <li key={todo.id}>{todo.description}</li>
      ))}
    </ul>
  );
}
