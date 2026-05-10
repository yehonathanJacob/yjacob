import { redis, pool } from './lib/db.js';
import { parseVoteData } from '../../shared/logic.js';

async function initDb() {
  const client = await pool.connect();
  try {
    await client.query(`
      CREATE TABLE IF NOT EXISTS votes (
        id VARCHAR(255) PRIMARY KEY,
        vote VARCHAR(255) NOT NULL
      );
    `);
    console.log('Database initialized');
  } catch (error) {
    console.error('Error initializing database:', error);
  } finally {
    client.release();
  }
}

async function processVotes() {
  console.log('Worker waiting for votes...');
  while (true) {
    try {
      const result = await redis.blpop('votes', 0);
      if (result) {
        const [key, data] = result;
        const { voter_id, vote } = parseVoteData(data);
        console.log(`Processing vote from ${voter_id}: ${vote}`);

        await pool.query(
          'INSERT INTO votes (id, vote) VALUES ($1, $2) ON CONFLICT (id) DO UPDATE SET vote = $2',
          [voter_id, vote]
        );
        console.log(`Vote saved to database`);
      }
    } catch (error) {
      console.error('Error processing vote:', error);
    }
  }
}

async function main() {
  await initDb();
  await processVotes();
}

main().catch(console.error);
