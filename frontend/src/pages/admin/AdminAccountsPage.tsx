import { useEffect, useState } from 'react'
import { Landmark, LogOut, ShieldCheck } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { AccountCard } from '../../components/accounts/AccountCard'
import { AccountDetailsModal } from '../../components/accounts/AccountDetailsModal'
import { initialAccounts, initialTransactions } from '../../data/mockData'
import type { Account } from '../../types/banking'
import { fetchAccounts, fetchTransactions, fetchUsers, getSessionUserId, logout, updateAccountStatus } from '../../api/bankingApi'
import type { Transaction } from '../../types/banking'

export function AdminAccountsPage() {
  const navigate = useNavigate()
  const sessionUserId = getSessionUserId()
  const [accounts, setAccounts] = useState(sessionUserId ? [] : initialAccounts)
  const [transactions, setTransactions] = useState<Transaction[]>(sessionUserId ? [] : initialTransactions)
  const [ownerNames, setOwnerNames] = useState<Record<string, string>>({})
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null)
  const [error, setError] = useState('')
  useEffect(() => { if (!sessionUserId) return; fetchAccounts(sessionUserId, true).then(setAccounts).catch(() => setError('Live admin data could not be loaded.')) }, [sessionUserId])
  useEffect(() => { if (!sessionUserId) return; fetchTransactions(sessionUserId).then(setTransactions).catch(() => setError('Live transaction history could not be loaded.')) }, [sessionUserId])
  useEffect(() => { if (!sessionUserId) return; fetchUsers().then((users) => setOwnerNames(Object.fromEntries(users.map((user) => [user.id, `${user.firstName} ${user.lastName}`])))).catch(() => setError('Account owners could not be loaded.')) }, [sessionUserId])
  const signOut = () => { logout(); navigate('/') }
  const toggleStatus = async (accountNumber: string) => { const account = accounts.find((item) => item.accountNumber === accountNumber); if (!account) return; if (!sessionUserId) { setAccounts((items) => items.map((item) => item.accountNumber === accountNumber ? { ...item, isActive: !item.isActive } : item)); return } try { const updated = await updateAccountStatus(sessionUserId, accountNumber, !account.isActive); setAccounts((items) => items.map((item) => item.accountNumber === accountNumber ? updated : item)); setSelectedAccount((item) => item?.accountNumber === accountNumber ? updated : item) } catch { setError('The account status could not be updated.') } }
  return <div className="app-shell admin-shell"><header className="topbar"><div className="brand"><Landmark size={22} /><span>Northstar Admin</span></div><div className="topbar-actions"><span className="admin-badge"><ShieldCheck size={15} /> Administrator</span><button className="signout-button" type="button" onClick={signOut}><LogOut size={17} /> Sign out</button></div></header><main className="page-content"><section className="welcome-row"><div><p className="eyebrow">ADMINISTRATION</p><h1>Account overview</h1><p className="subtitle">Review customer accounts and manage their active status.</p></div></section>{error && <p className="error-message">{error}</p>}<section className="account-section admin-accounts"><div className="section-heading"><div><p className="eyebrow">ALL CUSTOMER ACCOUNTS</p><h2>Accounts</h2></div><span>{accounts.length} accounts</span></div><div className="account-grid">{accounts.map((account) => <AccountCard key={account.accountNumber} account={account} admin ownerName={account.ownerId ? ownerNames[account.ownerId] : undefined} onSelect={setSelectedAccount} onToggleStatus={toggleStatus} />)}</div></section></main>{selectedAccount && <AccountDetailsModal account={selectedAccount} transactions={transactions} admin ownerName={selectedAccount.ownerId ? ownerNames[selectedAccount.ownerId] : undefined} onClose={() => setSelectedAccount(null)} />}</div>
}
