package smerge.ast;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Matcher {
	
	// smaller similarity = good
	private static final double SIM_THRESHOLD = 0.3;

		
	private List<Match> matches;
	private int nextID; // the next id to be given to a new matching

	public Matcher(AST baseTree, AST localTree, AST remoteTree) {	
		matches = new ArrayList<>();
		
		labelBaseTree(baseTree);
		match(baseTree, localTree, true);
		match(baseTree, remoteTree, false);
	}
	
	// match editTree's nodes to baseTree's
	// editTree is localTree if isLocal, otherwise editTree is remoteTree
	public void match(AST baseTree, AST editTree, boolean isLocal) {
		Set<Integer> matchedIDs = new HashSet<Integer>();
		matches.get(0).setEditNode(editTree.getRoot(), isLocal);
		matchedIDs.add(0);
		
		// compare each node in the baseTree to each node in editTree
		for (ASTNode base : baseTree) {
			if (matchedIDs.contains(base.getID())) continue;
			for (ASTNode edit : editTree) {
				
				// can't be matched, skip
				if (matchedIDs.contains(edit.getID()) || base.getType() != edit.getType()) 
					continue;
				
				if ((base.isLeafNode() && compareLeafNodes(base, edit)) ||
						(!base.isLeafNode() && compareInnerNodes(base, edit))) {
					// it's a match
					int id = base.getID();
					Match m = matches.get(id);
					m.setEditNode(edit, isLocal);
					matchedIDs.add(id);
					
					// do this now to detect conflicting actions early
					Differ.detectActions(matches, id, isLocal);
					
				} else {
					// not a match; create new one
					Match m = new Match(nextID);
					m.setEditNode(edit, isLocal);
					matches.add(m);
					nextID++;
				}
				
			}
		}
	}
	
	private void labelBaseTree(AST baseTree) {
		nextID = 0;
		for (ASTNode node : baseTree) {
			Match m = new Match(nextID);
			m.setBaseNode(node);
			matches.add(m);
			nextID++;
		}
	}
	
	// return true iff these leaf nodes should be matched
	private boolean compareLeafNodes(ASTNode n1, ASTNode n2) {
		double similarity = (double) distance(n1.getLabel(), n2.getLabel()) / Math.max(n1.getLabel().length(), n2.getLabel().length());
		return similarity <= SIM_THRESHOLD;
	}
	
	// return true iff these non-leaf nodes should be matched
	// in the future change to comparing nodes?
	private boolean compareInnerNodes(ASTNode n1, ASTNode n2) {
		return  n1.getLabel().equals(n2.getLabel());
	}
	
	// calculates Levenshtein distance between two strings
	private static int distance(String a, String b) {
	    a = a.toLowerCase();
	    b = b.toLowerCase();
	    // i == 0
	    int [] costs = new int [b.length() + 1];
	    for (int j = 0; j < costs.length; j++) {
	        costs[j] = j;
	    }
	    for (int i = 1; i <= a.length(); i++) {
	        // j == 0; nw = lev(i - 1, j)
	        costs[0] = i;
	        int nw = i - 1;
	        for (int j = 1; j <= b.length(); j++) {
	            int cj = Math.min(1 + Math.min(costs[j], costs[j - 1]), a.charAt(i - 1) == b.charAt(j - 1) ? nw : nw + 1);
	            nw = costs[j];
	            costs[j] = cj;
	        }
	    }
	    return costs[b.length()];
	}
	
	public List<Match> matches() {
		return matches;
	}
}