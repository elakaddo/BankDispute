import { apiGet } from "./client";

export interface Transaction {
  id: string;
  amount: number;
  currency: string;
  mti: string;
  stan: string;
  response_code: string;
  transaction_date: string;
  merchant_id: string;
  terminal_id: string | null;
  mcc: string;
  channel: string;
}

export function getTransactions(): Promise<Transaction[]> {
  return apiGet<Transaction[]>("/api/v1/transactions");
}