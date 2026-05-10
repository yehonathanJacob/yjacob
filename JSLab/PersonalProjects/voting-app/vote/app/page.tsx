'use client';

import { useState } from 'react';

export default function VotePage() {
  const [voted, setVoted] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleVote = async (option: string) => {
    setLoading(true);
    try {
      const response = await fetch('/api/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vote: option }),
      });

      if (response.ok) {
        setVoted(option);
      } else {
        alert('Failed to cast vote');
      }
    } catch (error) {
      console.error('Error voting:', error);
      alert('Error voting');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', textAlign: 'center', fontFamily: 'sans-serif' }}>
      <h1>Vote for your favorite!</h1>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginTop: '2rem' }}>
        <button
          onClick={() => handleVote('a')}
          disabled={loading || voted !== null}
          style={{
            padding: '1rem 2rem',
            fontSize: '1.5rem',
            cursor: loading || voted !== null ? 'not-allowed' : 'pointer',
            backgroundColor: voted === 'a' ? '#4caf50' : '#f0f0f0',
            border: '1px solid #ccc',
            borderRadius: '8px'
          }}
        >
          Option A (Cats)
        </button>
        <button
          onClick={() => handleVote('b')}
          disabled={loading || voted !== null}
          style={{
            padding: '1rem 2rem',
            fontSize: '1.5rem',
            cursor: loading || voted !== null ? 'not-allowed' : 'pointer',
            backgroundColor: voted === 'b' ? '#2196f3' : '#f0f0f0',
            border: '1px solid #ccc',
            borderRadius: '8px'
          }}
        >
          Option B (Dogs)
        </button>
      </div>
      {voted && (
        <p style={{ marginTop: '2rem', fontSize: '1.2rem', color: '#666' }}>
          Thanks for voting for <strong>{voted === 'a' ? 'Cats' : 'Dogs'}</strong>!
        </p>
      )}
    </div>
  );
}
