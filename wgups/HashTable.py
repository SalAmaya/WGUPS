class HashTable:
    def __init__(self, size=100):
        """
        Initialize the hash table with a specified size.
        Each slot in the table is a list to handle collisions using chaining.
        """
        self.size = size
        self.list = [[] for _ in range(size)]

    def insert(self, key, item):
        """
        Insert a key-value pair into the hash table.
        If the key already exists, update its value.
        """
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item # Update existing key
                return True
        
        key_value = [key, item]
        bucket_list.append(key_value) # Insert new key-value pair
        return True

    def lookup(self, key):
        """
        Lookup the value associated with the given key.
        Returns the value if found, or None if the key is not in the table.
        """
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        # search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1] # Return the value associated with the key
        return None # Key not found

    def remove(self, key):
        """
        Remove a key-value pair from the hash table.
        Returns True if the key was found and removed, or False if the key was not found.
        """
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
 
        for kv in bucket_list:
          if kv[0] == key:
              bucket_list.remove([kv[0],kv[1]])