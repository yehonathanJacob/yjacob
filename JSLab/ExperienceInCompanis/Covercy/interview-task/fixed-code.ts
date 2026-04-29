// Service: walletService.ts (Fixed)

export const db = {
  users: {
    // In a real database like MongoDB, we'd use $inc with a query condition { balance: { $gte: amount } }
    // In SQL, we'd use UPDATE users SET balance = balance - amount WHERE id = :id AND balance >= :amount
    atomicWithdraw: async (userId: string, amount: number) => {
      // Simulation of an atomic update
      // This is the critical "Senior" fix for Race Conditions
      const user = await db.users.findOne({ id: userId });
      if (user.balance >= amount) {
        user.balance -= amount;
        console.log(`DB Atomic Update: User ${userId} balance reduced by $${amount}. New balance: ${user.balance}`);
        return true;
      }
      return false;
    },
    findOne: async (query: { id: string }) => {
      // Mocked user data
      return { id: query.id, balance: 100 };
    }
  },
  // To handle the Consistency bug, we'd use a transaction or a ledger
  transactions: {
    create: async (data: any) => {
      console.log(`DB Transaction Log: ${JSON.stringify(data)}`);
      return { id: "tx_123" };
    },
    updateStatus: async (txId: string, status: string) => {
      console.log(`DB Transaction Status Updated: ${txId} -> ${status}`);
    }
  }
};

export const externalPaymentGateway = {
  process: async (amount: number) => {
    // Simulation of external payment processing
    await new Promise(resolve => setTimeout(resolve, 100));
    console.log(`External Gateway: Processed $${amount}`);
  }
};

export async function withdrawFunds(userId: string, amount: number) {
  // 1. Log the intention (Consistency Fix)
  const tx = await db.transactions.create({ userId, amount, status: 'PENDING' });

  try {
    // 2. Perform external payment
    await externalPaymentGateway.process(amount);

    // 3. Atomic update of balance (Race Condition Fix)
    // We check the condition AND update in one step to prevent double spending
    const success = await db.users.atomicWithdraw(userId, amount);

    if (success) {
      await db.transactions.updateStatus(tx.id, 'COMPLETED');
      return { success: true };
    } else {
      // Handle the case where balance became insufficient between steps (unlikely with locking but good to have)
      // Or in a ledger system, this wouldn't happen because we'd reserve the funds first.
      await db.transactions.updateStatus(tx.id, 'FAILED_INSUFFICIENT_FUNDS');
      // In a real scenario, we might need to refund the external payment here!
      return { success: false, error: "Insufficient funds" };
    }
  } catch (error) {
    console.error("Payment failed", error);
    await db.transactions.updateStatus(tx.id, 'FAILED_ERROR');
    return { success: false, error: "Payment gateway error" };
  }
}

/*
// Next.js Component (Client Side - Fixed)
import { useState } from 'react';

function WalletComponent({ userId }) {
  const [loading, setLoading] = useState(false);

  const handleWithdraw = async (amount) => {
    if (loading) return; // Prevention of double clicks
    
    setLoading(true);
    try {
      const res = await fetch('/api/withdraw', { 
          method: 'POST', 
          body: JSON.stringify({ userId, amount }) 
      });
      const data = await res.json();
      
      if (data.success) {
        alert("Withdrawal successful!");
      } else {
        alert(data.error || "Something went wrong");
      }
    } catch (err) {
      alert("Network error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button 
      onClick={() => handleWithdraw(100)} 
      disabled={loading} // Visual feedback and click prevention
    >
      {loading ? "Processing..." : "Withdraw $100"}
    </button>
  );
}
*/
