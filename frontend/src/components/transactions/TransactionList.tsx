import { ArrowLeftRight } from 'lucide-react'
import type { Transaction } from '../../types/banking'
import { formatMoney } from '../../data/mockData'
import { createWager, getSessionUserId } from '../../api/bankingApi'
import CoinFlip from '../coinflip/CoinFlip'

export function TransactionList({ transactions, onBalanceUpdated, wagersEnabled = true }: { transactions: Transaction[]; onBalanceUpdated?: (accountNumber: string, balance: number) => void; wagersEnabled?: boolean }) {
  const ownerId = getSessionUserId()

  return <div className="transaction-list">{transactions.map((transaction) => <div className="transaction-row" key={transaction.id}>
    <div className="transaction-icon"><ArrowLeftRight size={17} /></div>
    <div className="transaction-copy"><strong>{transaction.merchant}</strong><span>{transaction.category} · {transaction.date}</span></div>
    <div className="transaction-actions">
      <strong className={transaction.amount > 0 ? 'credit' : ''}>{formatMoney(transaction.amount)}</strong>
      {wagersEnabled && ownerId && transaction.amount < 0 && transaction.type === 'purchase' && <CoinFlip amount={Math.abs(transaction.amount)} currency="USD" initialResult={transaction.wagerResult === 'win' ? true : transaction.wagerResult === 'loss' ? false : null} onComplete={async () => {
        const wager = await createWager(transaction.id, ownerId)
        onBalanceUpdated?.(transaction.accountNumber, wager.updatedBalance)
        return wager.wagerResult === 'win'
      }} />}
    </div>
  </div>)}</div>
}
