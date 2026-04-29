// Race Condition Test Script

import * as buggy from './buggy-code.ts';
import * as fixed from './fixed-code.ts';

async function runBuggyTest() {
  console.log("\n--- RUNNING BUGGY VERSION TEST ---");
  // Shared state for the test
  let currentBalance = 100;
  
  // Overriding mocks to simulate real shared state and race condition
  (buggy.db.users.findOne as any) = async () => {
    console.log(`[Buggy] DB Read: Balance is ${currentBalance}`);
    return { id: 'user_1', balance: currentBalance };
  };
  
  (buggy.db.users.updateOne as any) = async (query: any, update: any) => {
    currentBalance = update.balance;
    console.log(`[Buggy] DB Write: Balance updated to ${currentBalance}`);
  };

  // Simulate 2 rapid clicks
  console.log("Simulating 2 concurrent withdrawal requests of $100 each...");
  const p1 = buggy.withdrawFunds('user_1', 100);
  const p2 = buggy.withdrawFunds('user_1', 100);

  const results = await Promise.all([p1, p2]);
  
  console.log("Results:", results);
  console.log(`Final Balance (Buggy): $${currentBalance}`);
  if (results.filter(r => r.success).length > 1) {
    console.error("BUG DETECTED: Two $100 withdrawals were successful from a $100 balance!");
  }
}

async function runFixedTest() {
  console.log("\n--- RUNNING FIXED VERSION TEST ---");
  let currentBalance = 100;

  // Overriding mocks for fixed version
  (fixed.db.users.findOne as any) = async () => {
    return { id: 'user_1', balance: currentBalance };
  };

  // The critical fix: atomic check-and-set
  (fixed.db.users as any).atomicWithdraw = async (userId: string, amount: number) => {
    if (currentBalance >= amount) {
      currentBalance -= amount;
      console.log(`[Fixed] Atomic DB Update: Success. New balance: ${currentBalance}`);
      return true;
    }
    console.log(`[Fixed] Atomic DB Update: FAILED. Insufficient funds. Balance: ${currentBalance}`);
    return false;
  };

  console.log("Simulating 2 concurrent withdrawal requests of $100 each...");
  const p1 = fixed.withdrawFunds('user_1', 100);
  const p2 = fixed.withdrawFunds('user_1', 100);

  const results = await Promise.all([p1, p2]);

  console.log("Results:", results);
  console.log(`Final Balance (Fixed): $${currentBalance}`);
  const successfulWithdrawals = results.filter(r => r.success).length;
  if (successfulWithdrawals === 1) {
    console.log("SUCCESS: Only one withdrawal was permitted.");
  } else {
    console.error(`FAILURE: Expected 1 successful withdrawal, but got ${successfulWithdrawals}`);
  }
}

async function main() {
  await runBuggyTest();
  await runFixedTest();
}

main().catch(console.error);
