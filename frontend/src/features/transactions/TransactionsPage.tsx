
import {useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ChevronDown, ChevronUp, Search, X } from "lucide-react";
import "./TransactionsStyle.css";
import { getTransactions, type Transaction } from "../../api/transactions";

type SortField = "transaction_date" | "amount";

function SortIcon({
    active,
    direction,
  }: {
    active: boolean;
    direction: "asc" | "desc";
  }) {
    if (!active) return <span className="sort-neutral">↕</span>;

    return direction === "asc" ? (
      <ChevronUp size={15} />
    ) : (
      <ChevronDown size={15} />
    );
}

function TransactionsPage() {
  const [selectedTransaction, setSelectedTransaction] =
    useState<Transaction | null>(null);
  const [searchId, setSearchId] = useState("");
  const [channelFilter, setChannelFilter] = useState("ALL");
  const [responseFilter, setResponseFilter] = useState("ALL");
  const [sortField, setSortField] = useState<SortField>("transaction_date");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("desc");
  const [currentPage, setCurrentPage] = useState(1);
  const PAGE_SIZE = 10;

  const {
    data: transactions = [],
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["transactions"],
    queryFn: getTransactions,
  });

  const channels = useMemo(
    () => [...new Set(transactions.map((t) => t.channel))].sort(),
    [transactions]
  );

  const responseCodes = useMemo(
    () => [...new Set(transactions.map((t) => t.response_code))].sort(),
    [transactions]
  );

  const filteredTransactions = useMemo(() => {
    const search = searchId.trim().toLowerCase();

    return transactions
      .filter((transaction) => {
        const matchesId = !search || transaction.id.toLowerCase().includes(search);
        const matchesChannel =
          channelFilter === "ALL" || transaction.channel === channelFilter;
        const matchesResponse =
          responseFilter === "ALL" ||
          transaction.response_code === responseFilter;

        return matchesId && matchesChannel && matchesResponse;
      })
      .sort((a, b) => {
        const comparison =
          sortField === "transaction_date"
            ? new Date(a.transaction_date).getTime() -
              new Date(b.transaction_date).getTime()
            : Number(a.amount) - Number(b.amount);

        return sortDirection === "asc" ? comparison : -comparison;
      });
  }, [
    transactions,
    searchId,
    channelFilter,
    responseFilter,
    sortField,
    sortDirection,
  ]);

  function handleSort(field: SortField) {
    if (sortField === field) {
      setSortDirection((current) => (current === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortDirection("desc");
    }
  }

  if (isLoading) {
    return <p>Chargement des transactions...</p>;
  }

  if (isError) {
    return (
      <p className="error-message">
        Impossible de charger les transactions : {error.message}
      </p>
    );
  }

  const totalPages = Math.ceil(filteredTransactions.length / PAGE_SIZE);

  const paginatedTransactions = filteredTransactions.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE
  );

  return (
    <section className="transactions-page">
      <div className="page-heading">
        <div>
          <h1>Transactions</h1>
          <p className="page-description">
            Consultation des transactions enregistrées.
          </p>
        </div>
      </div>

      <div className="transaction-toolbar">
        <div className="search-field">
          <Search size={17} />
          <input
            type="text"
            placeholder="Rechercher par identifiant..."
            value={searchId}
            onChange={(event) => {
              setSearchId(event.target.value);
              setCurrentPage(1);
            }}
          />
          {searchId && (
            <button
              className="clear-search"
              onClick={() => setSearchId("")}
              aria-label="Effacer la recherche"
            >
              <X size={15} />
            </button>
          )}
        </div>

        <select
          value={channelFilter}
          onChange={(event) => {{
              setChannelFilter(event.target.value)};
              setCurrentPage(1)
          }}
            
          aria-label="Filtrer par canal"
        >
          <option value="ALL">Tous les canaux</option>
          {channels.map((channel) => (
            <option key={channel} value={channel}>
              {channel}
            </option>
          ))}
        </select>

        <select
          value={responseFilter}
          onChange={(event) => {
            setResponseFilter(event.target.value);
             setCurrentPage(1);
          }}
          aria-label="Filtrer par code réponse"
        >
          <option value="ALL">Tous les codes réponse</option>
          {responseCodes.map((code) => (
            <option key={code} value={code}>
              {code}
            </option>
          ))}
        </select>

        <span className="results-count">
          {filteredTransactions.length} résultat(s)
        </span>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>
                <button
                  className="sort-button"
                  onClick={() => handleSort("transaction_date")}
                >
                  Date <SortIcon
                        active={sortField === "amount"}
                        direction={sortDirection}
                      />
                </button>
              </th>
              <th>Identifiant</th>
              <th>
                <button
                  className="sort-button"
                  onClick={() => handleSort("amount")}
                >
                  Montant <SortIcon
                          active={sortField === "amount"}
                          direction={sortDirection}
                        />
                </button>
              </th>
              <th>Commerçant</th>
              <th>Canal</th>
              <th>Code réponse</th>
            </tr>
          </thead>

          <tbody>
            {paginatedTransactions.map((transaction) => (
              <tr
                key={transaction.id}
                className="transaction-row"
                onClick={() => setSelectedTransaction(transaction)}
                tabIndex={0}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    setSelectedTransaction(transaction);
                  }
                }}
              >
                <td>
                  {new Date(transaction.transaction_date).toLocaleString("fr-FR")}
                </td>
                <td>{transaction.id.slice(0, 8)}</td>
                <td>
                  {transaction.amount} {transaction.currency}
                </td>
                <td>{transaction.merchant_id}</td>
                <td>{transaction.channel}</td>
                <td>{transaction.response_code}</td>
              </tr>
            ))}

            {filteredTransactions.length === 0 && (
              <tr>
                <td colSpan={6} className="empty-state">
                  Aucune transaction ne correspond à votre recherche.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="pagination">
      <span>
        Page {currentPage} sur {totalPages || 1}
      </span>

      <div>
        <button
          disabled={currentPage === 1}
          onClick={() => setCurrentPage((page) => page - 1)}
        >
          {"< "} Précédent 
        </button>

        <button
          disabled={currentPage >= totalPages}
          onClick={() => setCurrentPage((page) => page + 1)}
        >
         Suivant {" >"}
        </button>
      </div>
    </div>

      {selectedTransaction && (
        <div
          className="modal-overlay"
          onClick={() => setSelectedTransaction(null)}
        >
          <div
            className="transaction-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="transaction-modal-title"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="modal-header">
              <div>
                <h2 id="transaction-modal-title">
                  Détails de la transaction
                </h2>
                <span>
                  <b>ID complet</b> : {selectedTransaction.id}
                </span>
              </div>

              <button
                className="modal-close"
                onClick={() => setSelectedTransaction(null)}
                aria-label="Fermer"
              >
                <X size={20} />
              </button>
            </div>

            <div className="modal-content">
              <div className="detail-item">
                <span>Montant</span>
                <strong>
                  {selectedTransaction.amount} {selectedTransaction.currency}
                </strong>
              </div>
              <div className="detail-item">
                <span>Date</span>
                <strong>
                  {new Date(selectedTransaction.transaction_date).toLocaleString("fr-FR")}
                </strong>
              </div>
              <div className="detail-item">
                <span>MTI</span>
                <strong>{selectedTransaction.mti}</strong>
              </div>
              <div className="detail-item">
                <span>STAN</span>
                <strong>{selectedTransaction.stan}</strong>
              </div>
              <div className="detail-item">
                <span>Commerçant</span>
                <strong>{selectedTransaction.merchant_id}</strong>
              </div>
              <div className="detail-item">
                <span>Terminal</span>
                <strong>{selectedTransaction.terminal_id ?? "—"}</strong>
              </div>
              <div className="detail-item">
                <span>Canal</span>
                <strong>{selectedTransaction.channel}</strong>
              </div>
              <div className="detail-item">
                <span>Code réponse</span>
                <strong>{selectedTransaction.response_code}</strong>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export default TransactionsPage;
