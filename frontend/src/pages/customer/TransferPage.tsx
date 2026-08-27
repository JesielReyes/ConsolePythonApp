import { useState } from "react"
import {transferFunds} from "../../api/transactionApi"

export default function TransferPage() {

    const [fromAccount, setFromAccount] = useState<number | null>(null)
    const [fromErrorMsg, setfromErrorMsg] = useState<string | null>(null)
    const [toAccount, setToAccount] = useState<number | null>(null)
    const [toErrorMsg, setToErrorMsg] = useState<string | null>(null)
    const [amount, setAmount] = useState<number | null>(null)
    const [amountErrorMsg, setAmountErrorMsg] = useState<string | null>(null)
    const [toUserId, setUserId] = useState<string | null>(null)
    const [toUserIdErrorMsg, setUserIdErrorMsg] = useState<string | null>(null)

    function handleClick() {
        if (fromAccount === null) {
            setfromErrorMsg("Please select a from account")
            return
        }
        if (toUserId === null) {
            setUserIdErrorMsg("Please enter a user id")
            return
        }
        if (toAccount === null) {
            setToErrorMsg("Please enter a to account")
            return
        }
        if (amount === null || amount <= 0 ){
            setAmountErrorMsg("Please enter an amount")
            return
        }
        try {
            const response = transferFunds()
            console.log(response)
            if (response.status_code == 200) {
                alert("Transfer successful")
            } else {
                alert("Transfer failed")
            }
        } catch (error) {
            console.error(error)
            alert("Transfer failed")
        }
    }



    return (
        <div className="w-full h-full flex flex-col justify-center items-center">
            <div>
                <text>Transfer Portal</text>
            </div>
            <div className="w-[400px] h-[600px] flex flex-col justify-between bg-gray-100 rounded-2xl">
                <div className="pl-2 h-[50px] flex justify-center items-center w-[70px] bg-red-100 rounded-2xl">
                    <text>Back</text>
                </div>
                <div className="w-full flex-1 flex-col justify-center items-center px-2">
                    <div className="w-full flex-col h-1/4"> 
                        <div className="w-full flex flex-row justify-between items-center h-3/4">
                            <text>From Account:</text>
                            <input type="number" placeholder="Account Number" onChange={(e) => setFromAccount(e.target.valueAsNumber)} className="w-1/2 border border-gray-300 rounded-lg px-4 py-3"/>
                        </div>
                        <div className="w-full flex flex-1 flex-row justify-end items-center">
                            <text>{fromErrorMsg}</text>
                        </div>
                        
                    </div>


                    <div className="w-full flex-col h-1/4"> 
                        <div className="w-full flex flex-row justify-between items-center h-3/4">
                            <text>To User:</text>
                            <input type="number" placeholder="User Id" onChange={(e) => setUserId(e.target.value)} className="w-1/2 border border-gray-300 rounded-lg px-4 py-3"/>
                        </div>
                        <div className="w-full flex flex-1 flex-row justify-end items-center">
                            <text>{toUserIdErrorMsg}</text>
                        </div>
                    </div>

                    <div className="w-full flex-col h-1/4"> 
                        <div className="w-full flex flex-row justify-between items-center h-3/4">
                            <text>To User Account:</text>
                            <input type="number" placeholder="Account Number" onChange={(e) => setToAccount(e.target.valueAsNumber)} className="w-1/2 border border-gray-300 rounded-lg px-4 py-3"/>
                        </div>
                        <div className="w-full flex flex-1 flex-row justify-end items-center">
                            <text>{toErrorMsg}</text>
                        </div>
                    </div>

                    <div className="w-full flex-col h-1/4"> 
                        <div className="w-full flex flex-row justify-between items-center h-3/4">
                            <text>Amount $:</text>
                            <input type="number" placeholder="0" onChange={(e) => setAmount(e.target.valueAsNumber)} className="w-1/2 border border-gray-300 rounded-lg px-4 py-3" />
                        </div>
                        <div className="w-full flex flex-1 flex-row justify-end items-center">
                            <text>{amountErrorMsg}</text>
                        </div>
                    </div>
                </div>
                <div className="w-full bg-blue-100 flex justify-center items-center h-[50px] rounded-2xl" onClick={handleClick}>
                    <text>Transfer</text>
                </div>
            </div>
        </div>
    )
}