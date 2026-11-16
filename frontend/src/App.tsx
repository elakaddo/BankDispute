import { Navigate, Route, Routes } from "react-router-dom";
import AppShell from "./components/layout/AppShell";
import TransactionsPage from "./features/transactions/TransactionsPage";

function Supervision() {
  return (
    <section>
      <h1>Supervision</h1>
      <p className="page-description">
        Vue générale de votre activité.
      </p>

      <div className="summary-grid">
        <article className="summary-card">
          <span>Transactions</span>
          <strong>—</strong>
        </article>

        <article className="summary-card">
          <span>Alertes ouvertes</span>
          <strong>—</strong>
        </article>
      </div>
    </section>
  );
}

function Alerts() {
  return (
    <section>
      <h1>Alertes</h1>
      <p className="page-description">
        Consultez et gérez les alertes.
      </p>
      <div className="empty-state">
        Les alertes seront affichées ici.
      </div>
    </section>
  );
}

function Investigations() {
  return (
    <section>
      <h1>Investigations</h1>
      <p className="page-description">
        Espace de qualification et d'analyse des alertes.
      </p>
      <div className="empty-state">Fonctionnalité à venir.</div>
    </section>
  );
}

function Assistant() {
  return (
    <section>
      <h1>Assistant IA</h1>
      <p className="page-description">
        Assistant d'aide à l'analyse des alertes.
      </p>
      <div className="empty-state">Fonctionnalité à venir.</div>
    </section>
  );
}

function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<Supervision />} />
        <Route path="transactions" element={<TransactionsPage />} />
        <Route path="alerts" element={<Alerts />} />
        <Route path="investigations" element={<Investigations />} />
        <Route path="assistant" element={<Assistant />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

export default App;