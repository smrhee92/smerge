package smerge.ast;

import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.Stack;
import java.util.Iterator;
import java.util.LinkedList;

public abstract class ASTNode {
	
	// types that a node could be
	// two nodes can be matched only if they share the same type
	public enum Type {
		ROOT, IMPORT, WHITESPACE,
		CLASS, METHOD,
		IF_STATEMENT, WHILE_LOOP, FOR_LOOP,
		ASSIGNMENT, RETURN,
		COMMENT, BLOCK_COMMENT
	}
	
	protected Type type;
	protected String content;
	protected ASTNode parent;
	
	// we may need to change the way children are stored and added for merging purposes
	// such as ensuring children are at a specific position
	protected List<ASTNode> children;
	
	public int indentation; // unsure if needed
	
	private int id;

	public ASTNode() {
		this.type = Type.ROOT;
		this.children = new ArrayList<>();
		this.id = -1;
	}
	
	// most important method of this generic ASTNode:
	// all subtrees must be capable of unparsing themselves
	public abstract void unparse(StringBuilder sb);
	
	// attempts to merge the two given nodes into this node
	// should handle import merges
	// returns true iff these nodes are mergable
	public abstract boolean merge(ASTNode n1, ASTNode n2);
	
	public abstract void update(ASTNode edit);
	
	// returns the direct list of this node's children
	public List<ASTNode> children() {
		return children;
	}
	
	public ASTNode getParent() {
		return parent;
	}
	
	public void setParent(ASTNode parent) {
		this.parent = parent;
	}
	
	// adds the given child to this node ands sets this node as its parent
	// removes the child node from its original parent
	public void addChild(ASTNode child) {
		if (child.parent != null) child.parent.children.remove(child);
		children.add(child);
		child.parent = this;
	}
	
	public String getContent() {
		return content;
	}
	
	public void setContent(String content) {
		this.content = content;
	}
	
	public Type getType() {
		return type;
	}

	public boolean isRoot() {
		return indentation == -1;
	}
	public boolean isLeafNode() {
		return children.isEmpty();
	}
	
	
	public int getID() {
		return id;
	}

	public void setID(int id) {
		this.id = id;
	}
	
	public Iterator<ASTNode> preOrder() {
		return new NodeIterator(this);
	}
	
	// pre-order iterator starting with the given root
	private class NodeIterator implements Iterator<ASTNode> {
		
		private Stack<ASTNode> stack;
		
		public NodeIterator(ASTNode node) {
	        stack = new Stack<>();
			stack.push(node);
		}

		@Override
		public boolean hasNext() {
			return !stack.isEmpty();
		}

		@Override
		public ASTNode next() {
			ASTNode node = stack.pop();
			for (int i = node.children().size() - 1; i >= 0; i--) {
				stack.push(node.children().get(i));
			}
			return node;

		}
		
	}
	
	public String debugNode() {
		return "(" + id + ")" + indentation + content;
	}
	
	public void debugTree(StringBuilder sb, String indent) {
		String idString = "(" + id;
		if (parent != null) {
			idString += ":" + parent.getID() + "[" + parent.children.indexOf(this) + "]";
		}
		idString += ")";
		sb.append(idString + indent + content + "\n");
		for (ASTNode child : children) {
			child.debugTree(sb, indent + "    ");
		}
	}
	
	@Override
	public boolean equals(Object o) {
		if (o instanceof ASTNode) {
			return id == ((ASTNode) o).getID();
		}
		return false;
	}
	
	public String toString() {
		return "" + id;
	}
}
