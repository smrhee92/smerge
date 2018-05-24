package smerge.actions;

import smerge.ast.ASTNode;

public class Delete implements Action {
	
	private ASTNode child; // node to be deleted
	
	public Delete(ASTNode child) {
		this.child = child;
	}
	
	public int getPosition() {
		return child.getParent().children().indexOf(child);
	}
	
	public int getParentID() {
		return child.getParent().getID();
	}
	

	public void apply() {
		child.getParent().children().remove(child);
	}
	
	public String toString() {
		return "Delete " + child.getID();
	}

	
}