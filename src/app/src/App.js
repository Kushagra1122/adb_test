import './App.css';
import { TodoForm } from './components/TodoForm';
import { TodoList } from './components/TodoList';
import { useTodos } from './hooks/useTodos';

export function App() {
  const { todos, isLoading, isSubmitting, error, addTodo } = useTodos();

  return (
    <div className="App">
      <section className="panel">
        <h1>List of TODOs</h1>
        {error && <p className="error-text" role="alert">{error}</p>}
        <TodoList todos={todos} isLoading={isLoading} />
      </section>

      <section className="panel">
        <h1>Create a ToDo</h1>
        <TodoForm onSubmit={addTodo} isSubmitting={isSubmitting} />
      </section>
    </div>
  );
}

export default App;
