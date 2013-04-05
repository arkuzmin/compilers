package ru.arkuzmin.refactor;

import java.util.HashSet;
import java.util.Set;

public class Globals {
	
	public static final Set<Character> operations = new HashSet<Character>();
	
	static {
		operations.add('*');
		operations.add('[');
		operations.add(']');
		operations.add('&');
	}
	
	public interface StringConstants {
		String ENDLN = ";";
		String SPACE = " ";
		String EMPTY_STRING = "";
	}
	
	public interface SplitConstants {
		String VARS_SEPARATOR = ",";
	}
}
