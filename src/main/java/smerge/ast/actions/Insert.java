package smerge.ast.actions;

import smerge.ast.ASTNode;

public class Insert implements Action {
	
	private ASTNode parent; // node the child is inserted into (in base tree)
	private ASTNode child; // child introduced in edit tree (base if in move)
	private int position;
	
	public Insert(ASTNode parent, ASTNode child, int position) {
		if (child == null) throw new RuntimeException("null");
		this.parent = parent;
		this.child = child;
		this.position = position;
	}
	
	// inserts the sutree with root node under the given parent at the given position
	public void apply() {
		parent.children().add(position, child);
		child.setParent(parent);

	}
	
	public int getPosition() {
		return position;
	}
	
	// returns the id of the parent
	public int getParentID() {
		return parent.getID();
	}
	
	public ASTNode getChild() {
		return child;
	}
	
	public String toString() {
		return "Insert " + child.getID() + 
				"->" + parent.getID() + 
				"[" + position + "]";
	}

}
