import heapq


class MyStream:
	def __init__(self, iterator_list):
		"""
		iterator_list is a list of iterators, each having a .__next__() method that returns an integer, or raises a
		StopIteration exception if the stream is empty.
		"""
		self.hierarchy_in_order = ['value_of_item', 'index_of_iterator', 'index_in_list', 'head']
		self.heads = []
		counter_lists = 0
		for head in iterator_list:
			try:
				first_value = next(head)
			except StopIteration:
				continue  # case we got to end of an iterator
			pair = self.generate_pair(first_value, head, counter_lists)
			self.push_to_heads(pair)
			counter_lists += 1

	def __next__(self):
		"""
		Returns the minimal element among all next elements of the iterators in iterator_list
		"""
		new_value = self.pop_from_heads()
		return new_value

	def pop_from_heads(self):
		if len(self.heads) > 0:
			pair = heapq.heappop(self.heads)
			head = pair[self.get_index('head')]
			value_of_item = pair[self.get_index('value_of_item')]
			index_of_iterator = pair[self.get_index('index_of_iterator')]
			index_in_list = pair[self.get_index('index_in_list')]
			try:
				next_value = next(head)
				pair = self.generate_pair(next_value, head, index_of_iterator, index_in_list + 1)
				self.push_to_heads(pair)
			except StopIteration:
				pass  # case we got to end of an iterator
			return value_of_item
		else:
			raise StopIteration

	def push_to_heads(self, pair):
		heapq.heappush(self.heads, pair)

	def generate_pair(self, value, head, index_of_iterator, index_in_list=0):
		pair = list(range(len(self.hierarchy_in_order)))
		pair[self.get_index('value_of_item')] = value
		pair[self.get_index('index_of_iterator')] = index_of_iterator
		pair[self.get_index('index_in_list')] = index_in_list
		pair[self.get_index('head')] = head
		return pair

	def get_index(self,string):
		return self.hierarchy_in_order.index(string)

	def __iter__(self):
		return self
