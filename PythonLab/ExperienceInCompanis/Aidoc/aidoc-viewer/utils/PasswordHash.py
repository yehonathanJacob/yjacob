import bcrypt


class PasswordHash(object):
    def __init__(self, hash_):
        assert len(hash_) == 60, 'bcrypt hash should be 60 chars.'

        if isinstance(hash_, bytes):
            assert hash_.count(b'$'), 'bcrypt hash should have 3x "$".'
            self.hash = hash_.decode("utf-8")
        else:
            assert hash_.count('$'), 'bcrypt hash should have 3x "$".'
            self.hash = hash_

        self.rounds = int(self.hash.split('$')[2])

    def __eq__(self, candidate):
        """Hashes the candidate string and compares it to the stored hash."""
        if isinstance(candidate, str):
            hash_encoded = self.hash.encode('utf8')
            candidate = candidate.encode('utf8')
            return bcrypt.hashpw(candidate, hash_encoded) == hash_encoded
        return False

    def __repr__(self):
        """Simple object representation."""
        return '<{}>'.format(type(self).__name__)

    @classmethod
    def new(cls, password, rounds):
        """Creates a PasswordHash from the given password."""
        password = password.encode('utf8')
        return cls(bcrypt.hashpw(password, bcrypt.gensalt(rounds)))
