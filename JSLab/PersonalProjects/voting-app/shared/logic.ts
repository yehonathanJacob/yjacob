export function parseVoteData(data: string) {
  try {
    const parsed = JSON.parse(data);
    if (!parsed.voter_id || !parsed.vote) {
      throw new Error('Invalid vote data');
    }
    return parsed;
  } catch (error) {
    throw new Error('Failed to parse vote data');
  }
}
