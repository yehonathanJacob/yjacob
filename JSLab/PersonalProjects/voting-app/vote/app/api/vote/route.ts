import { NextResponse } from 'next/server';
import redis from '@/lib/redis';

export async function POST(request: Request) {
  try {
    const { vote } = await request.json();

    if (!vote) {
      return NextResponse.json({ error: 'Vote is required' }, { status: 400 });
    }

    const voterId = Math.random().toString(36).substring(7);
    const data = JSON.stringify({ voter_id: voterId, vote });

    await redis.rpush('votes', data);

    return NextResponse.json({ message: 'Vote recorded' });
  } catch (error) {
    console.error('Vote Error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
