class MonteCarloTreeSearch(object):

    def __init__(self, node):
        self.root = node

    def best_action(self, simulations_number):
        """

        Parameters
        ----------
        simulations_number : int
            number of simulations performed to get the best action

        Returns
        -------
        the move corresponding to the best child
        """
        for _ in range(0, simulations_number):            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        # to select best child go for exploitation only
        best_node = self.root.best_child(c_param=0.)

#============= CHANGED ================================#
        
        move = best_node.getCorrespondingMove()
        return move

#======================================================#

    def _tree_policy(self):
        """
        selects node to run rollout/playout for

        Returns
        -------
        the node not yet visited
        """
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
