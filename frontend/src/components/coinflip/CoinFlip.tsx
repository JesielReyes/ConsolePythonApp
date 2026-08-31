import { useState } from "react";

export interface CoinFlipProps {
	/** Amount that is at stake for this transaction. */
	amount: number;
	currency?: string;
	onComplete?: (amount: number, won: boolean) => void | boolean | Promise<boolean>;
	initialResult?: boolean | null;
	disabled?: boolean;
}

/** A small, self-contained double-or-nothing control for transaction rows. */
export default function CoinFlip({
	amount,
	currency = "USD",
	onComplete,
	initialResult = null,
	disabled = false,
}: CoinFlipProps) {
	const [flipping, setFlipping] = useState(false);
	const [result, setResult] = useState<boolean | null>(initialResult);
	const [error, setError] = useState(false);
	const completed = result !== null;

	const flip = () => {
		if (flipping || disabled || completed) return;

		setFlipping(true);
		setResult(null);
		setError(false);

		window.setTimeout(async () => {
			const won = Math.random() >= 0.5;
			try {
				const completedResult = await onComplete?.(won ? amount * 2 : 0, won);
				setResult(typeof completedResult === "boolean" ? completedResult : won);
			} catch {
				setError(true);
			} finally {
				setFlipping(false);
			}
		}, 700);
	};

	const formattedAmount = new Intl.NumberFormat(undefined, {
		style: "currency",
		currency,
	}).format(amount);

	return (
		<div className="coin-flip" style={{ textAlign: "center" }}>
			<button
				type="button"
				aria-label={completed ? "Wager already completed" : `Flip coin to double ${formattedAmount} or receive nothing`}
				aria-busy={flipping}
				disabled={disabled || flipping || completed}
				onClick={flip}
				style={{
					width: 52,
					height: 52,
					borderRadius: "50%",
					border: "3px solid #d49a24",
					background: "linear-gradient(145deg, #ffe58a, #d99b24)",
					color: "#6b4500",
					cursor: disabled || flipping || completed ? "default" : "pointer",
					fontWeight: 700,
					transform: flipping ? "rotateY(720deg)" : "rotateY(0deg)",
					transition: "transform 700ms ease-in-out, opacity 150ms ease",
					opacity: disabled ? 0.5 : 1,
				}}
			>
				{flipping ? "…" : result === null ? "½" : result ? "2×" : "0"}
			</button>
			<div aria-live="polite" style={{ marginTop: 6, fontSize: 12 }}>
				{result === null && !flipping && !error && `Double or nothing (${formattedAmount})`}
				{flipping && "Flipping…"}
				{result === true && `You won ${currency}${(amount * 2).toFixed(2)}!`}
				{result === false && "No payout this time."}
				{error && "Wager could not be completed."}
			</div>
		</div>
	);
}
