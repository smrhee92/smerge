package smerge.ast.actions;

import smerge.Merger;
import smerge.ast.ASTNode;

public class Update implements Action {
	
	private ASTNode base;
	private ASTNode local;
	private ASTNode remote;
	
	public Update(ASTNode base, ASTNode edit, boolean isLocal) {
		this.base = base;
		setEdit(edit, isLocal);
		
	}
	
	public void setEdit(ASTNode edit, boolean isLocal) {
		if (isLocal) {
			this.local = edit;
		} else {
			this.remote = edit;
		}
	}
	
	public ASTNode getEdit(boolean isLocal) {
		return isLocal ? local : remote;
	}
	// swap before with after
	public void apply() {
		if (local != null && remote != null) {
			Merger.totalConflicts++;
			boolean solved = base.merge(local, remote);
			if (solved) Merger.solvedConflicts++;
			
		} else if (local != null) {
			base.update(local);
		} else if (remote != null) {
			base.update(remote);
		}
	}
	
	public String toString() {
		return "Update " + base.getID();
	}

}
