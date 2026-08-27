import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { Plus, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { AccountCard } from '../../components/accounts/AccountCard'
import { AccountDetailsModal } from '../../components/accounts/AccountDetailsModal'
import { TransactionList } from '../../components/transactions/TransactionList'
import { currentUser, initialAccounts, initialTransactions } from '../../data/mockData'
import type { Account } from '../../types/banking'
import { createAccount, fetchAccounts, fetchTransactions, fetchUser, getSessionUserId } from '../../api/bankingApi'

export function DashboardPage() {
  const navigate = useNavigate()
  const sessionUserId = getSessionUserId()
  const [accounts, setAccounts] = useState(sessionUserId ? [] : initialAccounts)
  const [transactions, setTransactions] = useState(sessionUserId ? [] : initialTransactions)
  const [displayName, setDisplayName] = useState(`${currentUser.firstName} ${currentUser.lastName}`)
  const [error, setError] = useState('')
  useEffect(() => {
    if (!sessionUserId) return
    Promise.all([fetchAccounts(sessionUserId), fetchTransactions(sessionUserId), fetchUser(sessionUserId)])
      .then(([loadedAccounts, loadedTransactions, user]) => { setAccounts(loadedAccounts); setTransactions(loadedTransactions); setDisplayName(`${user.firstName} ${user.lastName}`) })
      .catch(() => setError('We could not load your live account data. Please try again.'))
  }, [sessionUserId])
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null)
  const [openAccountType, setOpenAccountType] = useState<'Checking' | 'Savings' | null>(null)
  const [openingDeposit, setOpeningDeposit] = useState('0')
  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'

  const openAccount = async (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); if (!sessionUserId || !openAccountType) return; if (Number(openingDeposit) < 0 || openingDeposit === '') { setError('Enter zero or a positive opening deposit.'); return } try { const account = await createAccount(sessionUserId, openAccountType, openingDeposit); setAccounts((items) => [...items, account]); setOpenAccountType(null); setOpeningDeposit('0') } catch { setError('The account could not be opened right now.') } }
  return <main className="page-content"><section className="welcome-row"><div><p className="eyebrow">PERSONAL BANKING</p><h1>{greeting}, {displayName.split(' ')[0]}</h1><p className="subtitle">Here is your financial snapshot.</p></div><div className="profile-chip"><span>JS</span><div><strong>{displayName}</strong><small>Customer</small></div></div></section>
    {error && <p className="error-message">{error}</p>}
    <section className="account-section"><div className="section-heading"><div><p className="eyebrow">YOUR ACCOUNTS</p><h2>Accounts</h2></div><span className="account-count">{accounts.length} accounts</span></div><div className="account-grid">
      {accounts.map((account) => <AccountCard key={account.accountNumber} account={account} onSelect={setSelectedAccount} />)}
      <article className="open-account-card"><h3>Grow your banking setup</h3><p>Open an account that fits the way you save and spend.</p><div className="open-account-actions"><button type="button" onClick={() => setOpenAccountType('Checking')}><Plus size={16} /> Checking</button><button type="button" onClick={() => setOpenAccountType('Savings')}><Plus size={16} /> Savings</button></div></article>
    </div></section>
    <section className="activity-preview"><div className="section-heading"><div><p className="eyebrow">LATEST ACTIVITY</p><h2>Recent transactions</h2></div><a href={`/account/${accounts[0]?.accountNumber ?? '8472'}`}>View all</a></div><TransactionList transactions={transactions.slice(0, 3)} /></section>
    {selectedAccount && <AccountDetailsModal account={selectedAccount} transactions={transactions} onClose={() => setSelectedAccount(null)} onWithdraw={(account) => navigate(`/account/${account.accountNumber}?withdraw=true`)} />}
    {openAccountType && <div className="modal-backdrop" role="presentation" onClick={() => setOpenAccountType(null)}><section className="account-modal open-account-modal" role="dialog" aria-modal="true" aria-labelledby="open-account-title" onClick={(event) => event.stopPropagation()}><div className="modal-header"><div><p className="eyebrow">NEW ACCOUNT</p><h2 id="open-account-title">Open {openAccountType.toLowerCase()}</h2></div><button className="icon-button" type="button" aria-label="Close account opening form" onClick={() => setOpenAccountType(null)}><X size={21} /></button></div><form className="form-panel account-opening-form" onSubmit={openAccount}><label htmlFor="opening-deposit">Opening deposit <span>(optional)</span></label><div className="money-input"><span>$</span><input id="opening-deposit" type="number" min="0" step="0.01" value={openingDeposit} onChange={(event) => setOpeningDeposit(event.target.value)} /></div><p className="form-hint">You can also add funds later from Deposit.</p><button className="primary-button" type="submit">Open {openAccountType.toLowerCase()} account</button></form></section></div>}
  </main>
}
