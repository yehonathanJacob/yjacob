import { NextResponse } from 'next/server';
import pool from '@/lib/db';

export async function GET() {
  try {
    const result = await pool.query('SELECT vote, COUNT(*) as count FROM votes GROUP BY vote');
    
    const results = result.rows.reduce((acc, row) => {
      acc[row.vote] = parseInt(row.count, 10);
      return acc;
    }, { a: 0, b: 0 });

    return NextResponse.json(results);
  } catch (error) {
    console.error('Results Error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
