import axios from 'axios'
import type { Account, AccountType, Transaction, User } from '../types/banking'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'
})


// Add JWT to every API request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('banking_access_token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})


export const getSessionUserId = () =>
  localStorage.getItem('banking_user_id')


export async function login(
  email: string,
  password: string
) {
  const response = await api.post('/login', {
    email,
    password
  })

  localStorage.setItem(
    'banking_access_token',
    response.data.access_token
  )

  localStorage.setItem(
    'banking_user_id',
    response.data.user_id
  )

  return {
    userId: response.data.user_id,
    isAdmin: response.data.is_admin
  }
}

export function logout() {
  localStorage.removeItem('banking_access_token')
  localStorage.removeItem('banking_user_id')
}

export async function createUser(user: { email: string; password: string; isAdmin: boolean; birthday: string; phoneNumber: string; firstName: string; lastName: string }) {
  const response = await api.post('/users', { email: user.email, password: user.password, is_admin: user.isAdmin, birthday: user.birthday, phone_number: user.phoneNumber, first_name: user.firstName, last_name: user.lastName })
  return response.data as { id: string; is_admin: boolean }
}

export async function isEmailAvailable(email: string) {
  const response = await api.get('/users')
  return !(response.data.users as { email: string }[]).some((user) => user.email.toLowerCase() === email.trim().toLowerCase())
}

const accountFromApi = (account: { account_number: number; account_type: AccountType; balance: number; created_date: string; is_active: boolean }): Account => ({
  accountNumber: String(account.account_number), accountType: account.account_type, balance: Number(account.balance), createdDate: account.created_date, isActive: account.is_active,
})

const transactionFromApi = (transaction: { id: number; from_owner_account_number: number; description?: string; amount: number; transaction_date: string; category?: string; type: string }): Transaction => ({
  id: String(transaction.id), merchant: transaction.description || transaction.type, date: new Date(transaction.transaction_date).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }), amount: transaction.type === 'deposit' ? Number(transaction.amount) : -Number(transaction.amount), category: transaction.category || transaction.type, accountNumber: String(transaction.from_owner_account_number),
})

export async function fetchUser(userId: string): Promise<User> {
  const response = await api.get(`/users/${userId}`)
  return { firstName: response.data.first_name, lastName: response.data.last_name, email: response.data.email, phoneNumber: response.data.phone_number, birthday: response.data.birthday }
}

export async function fetchAccounts(userId: string, admin = false): Promise<Account[]> {
  const response = await api.get('/accounts', { params: { requester_id: userId, ...(admin ? {} : { owner_id: userId }) } })
  return response.data.accounts.map(accountFromApi)
}

export async function fetchAccount(accountNumber: string): Promise<Account> {
  const response = await api.get(`/accounts/${accountNumber}`)
  return accountFromApi(response.data)
}

export async function fetchTransactions(userId: string): Promise<Transaction[]> {
  const response = await api.get('/transactions', { params: { owner_id: userId } })
  return response.data.map(transactionFromApi)
}

export async function createAccount(userId: string, accountType: AccountType, amount = '0') {
  const response = await api.post('/accounts', { owner_id: userId, account_type: accountType, amount }, { params: { requester_id: userId } })
  return accountFromApi(response.data)
}

export async function deposit(userId: string, accountNumber: string, amount: string, description?: string) {
  const response = await api.post('/transactions/deposit', { account_number: Number(accountNumber), amount, description }, { params: { owner_id: userId } })
  return accountFromApi(response.data)
}

export async function withdraw(userId: string, accountNumber: string, amount: string, description?: string) {
  const response = await api.post('/transactions/withdraw', { account_number: Number(accountNumber), amount, description }, { params: { owner_id: userId } })
  return accountFromApi(response.data)
}

export async function transfer(userId: string, fromAccountNumber: string, toAccountNumber: string, toOwnerId: string, amount: string) {
  return api.post('/transactions/transfer', { from_account_number: Number(fromAccountNumber), to_account_number: Number(toAccountNumber), to_owner_id: toOwnerId, amount }, { params: { owner_id: userId } })
}

export async function updateAccountStatus(requesterId: string, accountNumber: string, isActive: boolean) {
  const response = await api.patch(`/accounts/${accountNumber}/status`, { is_active: isActive }, { params: { requester_id: requesterId } })
  return accountFromApi(response.data)
}
