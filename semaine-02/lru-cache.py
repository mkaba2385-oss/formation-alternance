class Node:
    """
        Initialise un noeud de la liste doublement chaînée.

         Args:
            key (int) : Clé associée au nœud.
            value (int) : Valeur associée à la clé.

        Attributs :
            prev (Node | None) : Référence vers le noeud précédent.
            next (Node | None) : Référence vers le noeud suivant.
        """
    def __init__(self, key: int =0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        """
        Initialise un cache LRU de capacité limitée.

        Crée le dictionnaire contenant les éléments du cache ainsi que
        deux noeuds sentinelles (head et tail) permettant de simplifier
        les opérations sur la liste doublement chaînée.

        Args:
            capacity (int) : Nombre maximal d'éléments pouvant être stockés.

        Raises:
            ValueError : Levée si la capacité est inférieure ou égale à zéro.
        """

        if capacity <= 0:
            raise ValueError("la capacité doit etre positif")
        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node_to_head(self, node) -> None :
        """
        Ajoute un nœud juste après la tête de la liste.

        Le nœud devient ainsi le plus récemment utilisé.

        Args:
            node (Node) : Noeud à insérer.

        Complexité :
            O(1)
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """
        Supprime un noeud de la liste doublement chaînée.

        Les liens entre les noeuds précédent et suivant sont mis à jour
        afin de retirer le noeud de la liste.

        Args:
             node (Node) : Noeud à supprimer.

        Complexité :
             O(1)
        """
        prev_node = node.prev 
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node: Node) -> None:
        """
        Déplace un noeud en tête de la liste.

        Cette opération marque le noeud comme le plus récemment utilisé.

        Args:
            node (Node) : Nœud à déplacer.

        Complexité :
            O(1)
        """
        self._remove_node(node)
        self._add_node_to_head(node)

    def _pop_tail(self) -> Node:
        """
        Supprime et retourne le noeud le moins récemment utilisé.

        Le noeud retiré est celui situé juste avant le noeud sentinelle tail.

        Returns:
            Node : Le noeud supprimé.

        Complexité :
            O(1)
        """
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node
    
    def get(self, key: int):
        """
        Récupère la valeur associée à une clé du cache.

        Si la clé existe, le noeud correspondant est déplacé en tête
        de la liste afin d'être marqué comme récemment utilisé.

        Args:
            key (int) : Clé recherchée.

        Returns:
            int | None : La valeur associée à la clé si elle existe,
            sinon None.

        Complexité :
            O(1)
        """
        if key not in self.cache:
            return None
        else :
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        Ajoute une nouvelle entrée ou met à jour une entrée existante.

        Si la clé existe déjà sa valeur est mise à jour puis le noeud
        est déplacé en tête de liste. Si la capacité maximale est
        dépassée l'élément le moins récemment utilisé est supprimé.

        Args:
            key (int) : Clé à insérer ou à mettre à jour.
            value (int) : Valeur associée à la clé.

        Complexité :
            O(1)
        """
        if key in self.cache:
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node_to_head(new_node)
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]


# --- BONUS : Décorateur LRU Cache pour Fibonacci ---

def lru_cache_decorator(capacity):
    """
        Crée un décorateur utilisant un cache de type LRU.

        Le décorateur mémorise les résultats des appels d'une fonction
        afin d'éviter de recalculer plusieurs fois le même résultat.

        Args:
            capacity (int) : Nombre maximal de résultats à conserver.

        Returns:
            function : Le décorateur configuré avec la capacité indiquée.
        """
    def decorator(func):
        """
        Applique un cache LRU à une fonction.

        Une nouvelle instance de LRUCache est créée pour la fonction
        décorée.

        Args:
            func (function) : Fonction à décorer.

        Returns:
            function : Fonction enveloppée par le mécanisme de cache.
        """
        cache = LRUCache(capacity)

        def wrapper(*args):
            """
            Intercepte les appels à la fonction décorée.

            Vérifie si le résultat correspondant aux arguments est déjà
            présent dans le cache. Si ce n'est pas le cas, la fonction est
            exécutée et son résultat est mémorisé avant d'être renvoyé.

            Args:
                *args : Arguments transmis à la fonction décorée.

            Returns:
                Any : Résultat de la fonction, récupéré depuis le cache
                ou calculé si nécessaire.
            """
            key = args[0]
            result = cache.get(key)
            if result is None:
                result = func(*args)
                cache.put(key, result)
            return result
        wrapper.cache_instance = cache
        return wrapper
    return decorator

