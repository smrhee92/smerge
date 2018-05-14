package smerge.ast.parsers;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.Scanner;

import smerge.ast.AST;
import smerge.ast.parsers.python.PythonParser;

public interface Parser {
	
	public static Parser getInstance(String filename) {
		// if filename.endsWith(".py")?
		return new PythonParser();
	}
	
	public AST parse(String filename) throws IOException;
	
}
