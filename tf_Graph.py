#!/usr/bin/env python
# coding: utf-8

# In[2]:
import numpy as np

class Graph():
    def __init__(self):
        self.operations = []
        self.placeholders = []
        self.variables = []
        self.constants = []

    def as_default(self):
        global _default_graph
        _default_graph = self


# In[1]:


class Operation():
    def __init__(self, input_nodes=None):
        self.input_nodes = input_nodes
        self.output = None

        # Append operation to the list of operations of the default graph
        _default_graph.operations.append(self)
    def forward(self):
        pass

    def backward(self):
        pass


# In[5]:


class BinaryOperation(Operation):
    def __init__(self, a, b):
        super().__init__([a, b])


# In[6]:


class add(BinaryOperation):
  """
  Computes a + b, element-wise
  """
  def forward(self, a, b):
    return a + b

  def backward(self, upstream_grad):
    raise NotImplementedError

class multiply(BinaryOperation):
  """
  Computes a * b, element-wise
  """
  def forward(self, a, b):
    return a * b

  def backward(self, upstream_grad):
    raise NotImplementedError

class divide(BinaryOperation):
  """
  Returns the true division of the inputs, element-wise
  """
  def forward(self, a, b):
    return np.true_divide(a, b)

  def backward(self, upstream_grad):
    raise NotImplementedError

class matmul(BinaryOperation):
  """
  Multiplies matrix a by matrix b, producing a * b
  """
  def forward(self, a, b):
    return a.dot(b)

  def backward(self, upstream_grad):
    raise NotImplementedError


# In[7]:


class Placeholder():
    def __init__(self):
        self.value = None
        _default_graph.placeholders.append(self)


# In[8]:


class Constant():
    def __init__(self, value=None):
        self.__value = value
        _default_graph.constants.append(self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        raise ValueError("Cannot reassign value.")


# In[9]:


class Variable():
    def __init__(self, initial_value=None):
        self.value = initial_value
        _default_graph.variables.append(self)


# In[10]:


def topology_sort(operation):
    ordering = []
    visited_nodes = set()

    def recursive_helper(node):
      if isinstance(node, Operation):
        for input_node in node.input_nodes:
          if input_node not in visited_nodes:
            recursive_helper(input_node)

      visited_nodes.add(node)
      ordering.append(node)

    # start recursive depth-first search
    recursive_helper(operation)

    return ordering
# In[11]:


class Session():
    def run(self, operation, feed_dict={}):
        nodes_sorted = topology_sort(operation)

        for node in nodes_sorted:
            if type(node) == Placeholder:
                node.output = feed_dict[node]
            elif type(node) == Variable or type(node) == Constant:
                node.output = node.value
            else:
                inputs = [node.output for node in node.input_nodes]
                node.output = node.forward(*inputs)

        return operation.output


# In[ ]:




