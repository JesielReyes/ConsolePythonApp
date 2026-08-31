import { useEffect, useState } from 'react'
import { ArrowLeftRight } from 'lucide-react'
import type { Transaction } from '../../types/banking'
import { formatMoney } from '../../data/mockData'
import { createWager, fetchTransactionCategories, getSessionUserId, updateTransactionCategory } from '../../api/bankingApi'
import CoinFlip from '../coinflip/CoinFlip'

export function TransactionList({ transactions, onBalanceUpdated, onWagerCreated, wagersEnabled = true, categoriesEnabled = true }: { transactions: Transaction[]; onBalanceUpdated?: (accountNumber: string, balance: number) => void; onWagerCreated?: (transactionId: string, result: 'win' | 'loss') => void; wagersEnabled?: boolean; categoriesEnabled?: boolean }) {
  const ownerId = getSessionUserId()
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCategories, setSelectedCategories] = useState<Record<string, string>>({})

  useEffect(() => {
    if (!ownerId || !categoriesEnabled) return
    fetchTransactionCategories(ownerId).then(setCategories).catch(() => setCategories([]))
  }, [categoriesEnabled, ownerId])

  const changeCategory = async (transaction: Transaction, category: string) => {
    if (!ownerId) return
    const previousCategory = selectedCategories[transaction.id] ?? transaction.category ?? ''
    setSelectedCategories((current) => ({ ...current, [transaction.id]: category }))
    try {
      await updateTransactionCategory(transaction.id, ownerId, category || undefined)
    } catch {
      setSelectedCategories((current) => ({ ...current, [transaction.id]: previousCategory }))
    }
  }

  return <div className="transaction-list">{transactions.map((transaction) => <div className="transaction-row" key={transaction.id}>
    <div className="transaction-icon"><ArrowLeftRight size={17} /></div>
    <div className="transaction-copy"><strong>{transaction.merchant}</strong><span>{selectedCategories[transaction.id] || 'None'} · {transaction.date}</span>{categoriesEnabled && <select className="transaction-category" aria-label={`Category for ${transaction.merchant}`} value={selectedCategories[transaction.id] ?? transaction.category ?? ''} onChange={(event) => changeCategory(transaction, event.target.value)}><option value="">None</option>{categories.map((category) => <option key={category} value={category}>{category}</option>)}</select>}</div>
    <div className="transaction-actions">
      <strong className={transaction.amount > 0 ? 'credit' : ''}>{formatMoney(transaction.amount)}</strong>
      {wagersEnabled && ownerId && transaction.amount < 0 && transaction.type === 'purchase' && <CoinFlip amount={Math.abs(transaction.amount)} currency="USD" initialResult={transaction.wagerResult === 'win' ? true : transaction.wagerResult === 'loss' ? false : null} onComplete={async () => {
        const wager = await createWager(transaction.id, ownerId)
        onBalanceUpdated?.(transaction.accountNumber, wager.updatedBalance)
        onWagerCreated?.(transaction.id, wager.wagerResult)
        return wager.wagerResult === 'win'
      }} />}
    </div>
  </div>)}</div>
}
