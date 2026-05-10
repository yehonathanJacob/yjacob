// Service: walletService.ts
// המשימה למועמד:
// "לפניך קוד שמטפל במשיכת כספים מארנק דיגיטלי ב-Node.js. יש כאן באגים שעלולים לגרום לאובדן כספי או לחוויית משתמש גרועה. זהה אותם ותקן."

export const db = {
  users: {
    findOne: async (query: { id: string }) => {
      // Mocking a slow database read
      return { id: query.id, balance: 100 };
    },
    updateOne: async (query: { id: string }, update: any) => {
      // Mocking a database update
      console.log(`DB Update: User ${query.id} new balance ${update.balance}`);
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
  const user = await db.users.findOne({ id: userId });

  if (user.balance >= amount) {
    // סימולציה של עיבוד תשלום חיצוני
    await externalPaymentGateway.process(amount); 

    const newBalance = user.balance - amount;
    await db.users.updateOne({ id: userId }, { balance: newBalance });
    
    return { success: true };
  }

  return { success: false, error: "Insufficient funds" };
}

/*
// Next.js Component (Client Side)
import { useState } from 'react';

function WalletComponent({ userId }) {
  const [loading, setLoading] = useState(false);

  const handleWithdraw = async (amount) => {
    setLoading(true);
    const res = await fetch('/api/withdraw', { 
        method: 'POST', 
        body: JSON.stringify({ userId, amount }) 
    });
    const data = await res.json();
    
    if (data.success) {
      alert("Withdrawal successful!");
    }
    setLoading(false);
  };

  return <button onClick={() => handleWithdraw(100)}>Withdraw $100</button>;
}
*/
